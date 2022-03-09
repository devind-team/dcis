<template lang="pug">
  node-view-wrapper
    span.image-view(draggable="true" data-drag-handle)
      div.image-view__body(:class="{'image-view__body--focused': selected, 'image-view__body--resizing': isResizing}")
        img.image-view__body__image.ma-0(
          :src="node.attrs.src"
          :style="`width: ${width}px; height: ${height}px;`"
          @click="selectImage")
        div.image-resizer(v-show="selected || isResizing")
          span.image-resizer__handler(v-for="direction in resizeDirections" :key="direction"
            :class="`image-resizer__handler--${direction}`" @mousedown="onMouseDown($event, direction)")
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { NodeViewWrapper } from '@tiptap/vue-2'
import { Node as ProseMirrorNode } from 'prosemirror-model'
import { Editor } from '@tiptap/core'
import { NodeSelection } from 'prosemirror-state'
import { resolveImg } from '~/components/common/editor/extensions/nativeExtensions/image/utils'

const MIN_SIZE = 20
const MAX_SIZE = 100000

const enum ResizeDirection {
  TOP_LEFT = 'tl',
  TOP_RIGHT = 'tr',
  BOTTOM_LEFT = 'bl',
  BOTTOM_RIGHT = 'br'
}

export default Vue.extend<any, any, any, any>({
  components: { NodeViewWrapper },
  props: {
    node: { type: ProseMirrorNode, required: true },
    editor: { type: Object as PropType<Editor>, required: true },
    getPos: { type: Function, required: true },
    updateAttributes: { type: Function, required: true },
    selected: { type: Boolean, required: true },
    extension: { type: Object, required: true }
  },
  data: () => ({
    isResizing: false,
    resizeDirections: [
      ResizeDirection.TOP_LEFT,
      ResizeDirection.TOP_RIGHT,
      ResizeDirection.BOTTOM_LEFT,
      ResizeDirection.BOTTOM_RIGHT
    ],
    maxSize: {
      width: MAX_SIZE,
      height: MAX_SIZE
    },
    originalSize: {
      width: 0,
      height: 0
    },
    resizerState: {
      x: 0,
      y: 0,
      w: 0,
      h: 0,
      dir: ''
    }
  }),
  computed: {
    width (): number {
      if (this.node.attrs.sizeMode === '%') {
        return this.originalSize.width * this.node.attrs.width / 100
      }
      return this.node.attrs.width
    },
    keepAspectRatio (): boolean {
      return this.node.attrs.keepAspectRatio
    },
    aspectRatio (): number {
      return this.originalSize.width / this.originalSize.height
    },
    height (): number {
      if (this.keepAspectRatio) {
        return this.width / this.aspectRatio
      }
      if (this.node.attrs.sizeMode === '%') {
        return this.originalSize.height * this.node.attrs.height / 100
      } else {
        return this.node.attrs.height
      }
    }
  },
  mounted () {
    this.getImgSize(this.node.attrs.src)
  },
  methods: {
    selectImage (): void {
      const { view } = this.editor
      const { state } = view
      let { tr } = state
      const selection = NodeSelection.create(state.doc, this.getPos())
      tr = tr.setSelection(selection)
      view.dispatch(tr)
    },
    async getImgSize (imgSrc: string) {
      const result = await resolveImg(imgSrc)
      this.originalSize = {
        width: result.width,
        height: result.height
      }
    },
    onMouseDown (e: MouseEvent, dir: ResizeDirection): void {
      e.preventDefault()
      e.stopPropagation()
      this.resizerState.x = e.clientX
      this.resizerState.y = e.clientY
      const originalWidth = this.originalSize.width
      const originalHeight = this.originalSize.height
      const aspectRatio = originalWidth / originalHeight
      let width = this.width
      let height = this.height
      const maxWidth = this.maxSize.width
      if (width && !height) {
        width = width > maxWidth ? maxWidth : width
        height = Math.round(width / aspectRatio)
      } else if (height && !width) {
        width = Math.round(height * aspectRatio)
        width = width > maxWidth ? maxWidth : width
      } else if (!width && !height) {
        width = originalWidth > maxWidth ? maxWidth : originalWidth
        height = Math.round(width / aspectRatio)
      } else {
        width = width > maxWidth ? maxWidth : width
      }
      this.resizerState.w = width
      this.resizerState.h = height
      this.resizerState.dir = dir
      this.isResizing = true
      this.onEvents()
    },
    onMouseMove (e: MouseEvent): void {
      e.preventDefault()
      e.stopPropagation()
      if (!this.isResizing) {
        return
      }
      const { x, y, w, h, dir } = this.resizerState
      const dx = (e.clientX - x) * (/l/.test(dir) ? -1 : 1)
      const dy = (e.clientY - y) * (/t/.test(dir) ? -1 : 1)
      this.updateAttrs(
        Math.max(Math.min(w + dx, this.maxSize.width), MIN_SIZE), // clamp(w + dx, MIN_SIZE, this.maxSize.width),
        Math.max(h + dy, MIN_SIZE))
    },
    updateAttrs (width: number, height: number) {
      if (this.keepAspectRatio) {
        height = width / this.aspectRatio
      }
      if (this.node.attrs.sizeMode === '%') {
        width = width * 100 / this.originalSize.width
        height = height * 100 / this.originalSize.height
      }
      this.updateAttributes({ width, height })
    },
    onMouseUp (e: MouseEvent): void {
      e.preventDefault()
      e.stopPropagation()
      if (!this.isResizing) {
        return
      }
      this.isResizing = false
      this.resizerState = {
        x: 0,
        y: 0,
        w: 0,
        h: 0,
        dir: ''
      }
      this.offEvents()
      this.selectImage()
    },
    onEvents (): void {
      document.addEventListener('mousemove', this.onMouseMove, true)
      document.addEventListener('mouseup', this.onMouseUp, true)
    },
    offEvents (): void {
      document.removeEventListener('mousemove', this.onMouseMove, true)
      document.removeEventListener('mouseup', this.onMouseUp, true)
    }
  }
})
</script>

<style lang="sass">
img
  display: inline-block
  float: none
  margin: 12px 0
  max-width: 100%

  &[data-display=inline]
    margin-left: 12px
    margin-right: 12px

  &[data-display=block]
    display: block

  &[data-display=left]
    float: left
    margin-left: 0
    margin-right: 12px

  &[data-display=right]
    float: right
    margin-left: 12px
    margin-right: 0

.image-view
  $root: &

  display: inline-block
  float: none
  line-height: 0
  margin: 12px 0
  max-width: 100%
  user-select: none
  vertical-align: baseline

  &--inline
    margin-left: 12px
    margin-right: 12px

  &--block
    display: block

  &--left
    float: left
    margin-left: 0
    margin-right: 12px

  &--right
    float: right
    margin-left: 12px
    margin-right: 0

  &__body
    clear: both
    display: inline-block
    max-width: 100%
    outline: transparent solid 2px
    transition: all .2s ease-in
    position: relative

    &:hover
      outline-color: #ffc83d

    &--focused:hover,
    &--resizing:hover
      outline-color: transparent

    &__placeholder
      height: 100%
      left: 0
      position: absolute
      top: 0
      width: 100%
      z-index: -1

    &__image
      cursor: pointer
      margin: 0

.image-resizer
  border: 1px solid cornflowerblue
  height: 100%
  left: 0
  position: absolute
  top: 0
  width: 100%
  z-index: 1

  &__handler
    background-color: cornflowerblue
    border: 1px solid white
    border-radius: 2px
    box-sizing: border-box
    display: block
    height: 12px
    position: absolute
    width: 12px
    z-index: 2

    &--tl
      cursor: nw-resize
      left: -6px
      top: -6px

    &--tr
      cursor: ne-resize
      right: -6px
      top: -6px

    &--bl
      bottom: -6px
      cursor: sw-resize
      left: -6px

    &--br
      bottom: -6px
      cursor: se-resize
      right: -6px
</style>
