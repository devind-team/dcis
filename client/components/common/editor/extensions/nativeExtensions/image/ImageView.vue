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
import { defineComponent, PropType, ref, computed, onMounted } from '#app'
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

export default defineComponent({
  components: { NodeViewWrapper },
  props: {
    node: { type: ProseMirrorNode, required: true },
    editor: { type: Object as PropType<Editor>, required: true },
    getPos: { type: Function as PropType<() => number>, required: true },
    updateAttributes: { type: Function as PropType<({ width, height }) => void>, required: true },
    selected: { type: Boolean, required: true },
    extension: { type: Object, required: true }
  },
  setup (props) {
    const isResizing = ref(false)
    const maxSize = ref({ width: MAX_SIZE, height: MAX_SIZE })
    const originalSize = ref({ width: 0, height: 0 })
    const resizerState = ref({ x: 0, y: 0, w: 0, h: 0, dir: '' })
    const resizeDirections = ref([ResizeDirection.TOP_LEFT,
      ResizeDirection.TOP_RIGHT,
      ResizeDirection.BOTTOM_LEFT,
      ResizeDirection.BOTTOM_RIGHT
    ])

    const width = computed(() => {
      if (props.node.attrs.sizeMode === '%') {
        return originalSize.value.width * props.node.attrs.width / 100
      }
      return props.node.attrs.width
    })
    const keepAspectRatio = computed(() => {
      return props.node.attrs.keepAspectRatio
    })
    const aspectRatio = computed(() => {
      return originalSize.value.width / originalSize.value.height
    })
    const height = computed(() => {
      if (keepAspectRatio.value) {
        return width.value / aspectRatio.value
      }
      if (props.node.attrs.sizeMode === '%') {
        return originalSize.value.height * props.node.attrs.height / 100
      } else {
        return props.node.attrs.height
      }
    })

    const selectImage = () => {
      const { view } = props.editor
      const { state } = view
      let { tr } = state
      const selection = NodeSelection.create(state.doc, props.getPos())
      tr = tr.setSelection(selection)
      view.dispatch(tr)
    }
    const getImgSize = async (imgSrc: string) => {
      const result = await resolveImg(imgSrc)
      originalSize.value = {
        width: result.width,
        height: result.height
      }
    }
    const updateAttrs = (width: number, height: number) => {
      if (keepAspectRatio.value) {
        height = width / aspectRatio.value
      }
      if (props.node.attrs.sizeMode === '%') {
        width = width * 100 / originalSize.value.width
        height = height * 100 / originalSize.value.height
      }
      props.updateAttributes({ width, height })
    }
    const onMouseMove = (e: MouseEvent) => {
      e.preventDefault()
      e.stopPropagation()
      if (!isResizing.value) {
        return
      }
      const { x, y, w, h, dir } = resizerState.value
      const dx = (e.clientX - x) * (/l/.test(dir) ? -1 : 1)
      const dy = (e.clientY - y) * (/t/.test(dir) ? -1 : 1)
      updateAttrs(
        Math.max(Math.min(w + dx, maxSize.value.width), MIN_SIZE), // clamp(w + dx, MIN_SIZE, this.maxSize.width),
        Math.max(h + dy, MIN_SIZE))
    }
    const offEvents = () => {
      document.removeEventListener('mousemove', onMouseMove, true)
      document.removeEventListener('mouseup', onMouseUp, true)
    }
    const onMouseUp = (e: MouseEvent) => {
      e.preventDefault()
      e.stopPropagation()
      if (!isResizing.value) {
        return
      }
      isResizing.value = false
      resizerState.value = {
        x: 0,
        y: 0,
        w: 0,
        h: 0,
        dir: ''
      }
      offEvents()
      selectImage()
    }
    const onEvents = () => {
      document.addEventListener('mousemove', onMouseMove, true)
      document.addEventListener('mouseup', onMouseUp, true)
    }
    const onMouseDown = (e: MouseEvent, dir: ResizeDirection) => {
      e.preventDefault()
      e.stopPropagation()
      resizerState.value.x = e.clientX
      resizerState.value.y = e.clientY
      const originalWidth = originalSize.value.width
      const originalHeight = originalSize.value.height
      const aspectRatio = originalWidth / originalHeight
      let _width = width.value
      let _height = height.value
      const maxWidth = maxSize.value.width
      if (_width && !_height) {
        _width = _width > maxWidth ? maxWidth : _width
        _height = Math.round(_width / aspectRatio)
      } else if (_height && !_width) {
        _width = Math.round(_height * aspectRatio)
        _width = _width > maxWidth ? maxWidth : _width
      } else if (!_width && !_height) {
        _width = originalWidth > maxWidth ? maxWidth : originalWidth
        _height = Math.round(_width / aspectRatio)
      } else {
        _width = _width > maxWidth ? maxWidth : _width
      }
      resizerState.value.w = _width
      resizerState.value.h = _height
      resizerState.value.dir = dir
      isResizing.value = true
      onEvents()
    }

    onMounted(() => {
      getImgSize(props.node.attrs.src)
    })
    return {
      isResizing,
      maxSize,
      originalSize,
      resizerState,
      resizeDirections,
      width,
      keepAspectRatio,
      aspectRatio,
      height,
      selectImage,
      getImgSize,
      updateAttrs,
      onMouseMove,
      onMouseDown
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
