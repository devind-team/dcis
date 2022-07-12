<template lang="pug">
client-only
  v-card(:class="{ 'fullscreen': isFullscreen }")
    v-card-title(v-if="!preview" flat dense)
      template(v-for="action in toolbarActions")
        component(:is="action.component.type" v-bind="action.render" :editor="editor")
      v-spacer
      v-tooltip(top)
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" @click="editor.commands.undo()" icon)
            v-icon mdi-undo
        span {{$t('common.richTextEditor.undo')}}
      v-tooltip(top)
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" @click="editor.commands.redo()" icon)
            v-icon mdi-redo
        span {{$t('common.richTextEditor.redo')}}
      v-tooltip(top)
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" @click="toggleFullscreen" icon)
            v-icon {{`${isFullscreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'}`}}
        span {{`${isFullscreen ? $t('common.richTextEditor.fullscreenExit') : $t('common.richTextEditor.fullscreen')}`}}
    v-card-text
      bubble-menu(v-if="editor" :shouldShow="() => true" :editor="editor")
        v-card
          template(v-for="action in bubbleActions")
            component(:is="action.component.type" v-bind="action.render" :editor="editor")
      editor-typography
        v-sheet(v-show="!preview")
          editor-content.editor_content(:editor="editor")
        v-sheet(v-show="preview" v-html="editor ? editor.getHTML() : ''")
    v-card-actions
      v-checkbox(v-model="preview" :label="$t('common.richTextEditor.preview')")
</template>

<script lang="ts">
import { defineComponent, PropType, ref, onMounted, onBeforeUnmount } from '#app'
import { Editor, EditorContent, BubbleMenu } from '@tiptap/vue-2'
import { Editor as CoreEditor } from '@tiptap/core'
import { Document } from '@tiptap/extension-document'
import { Text } from '@tiptap/extension-text'
import { TextStyle } from '@tiptap/extension-text-style'
import { Paragraph } from '@tiptap/extension-paragraph'
import { History } from '@tiptap/extension-history'
import { Gapcursor } from '@tiptap/extension-gapcursor'
import { Dropcursor } from '@tiptap/extension-dropcursor'
import { ListItem } from '@tiptap/extension-list-item'
import Bold from '~/components/common/editor/extensions/nativeExtensions/Bold'
import Italic from '~/components/common/editor/extensions/nativeExtensions/Italic'
import TextAlign from '~/components/common/editor/extensions/nativeExtensions/TextAlign'
import File from '~/components/common/editor/extensions/nativeExtensions/File'
import Image from '~/components/common/editor/extensions/nativeExtensions/Image'
import OrderedList from '~/components/common/editor/extensions/nativeExtensions/OrderedList'
import BulletList from '~/components/common/editor/extensions/nativeExtensions/BulletList'
import Highlight from '~/components/common/editor/extensions/nativeExtensions/Highlight'
import Table from '~/components/common/editor/extensions/nativeExtensions/Table'
import Strike from '~/components/common/editor/extensions/nativeExtensions/Strike'
import Link from '~/components/common/editor/extensions/nativeExtensions/Link'
import HTML from '~/components/common/editor/extensions/nativeExtensions/HTML'
import LineHeight from '~/components/common/editor/extensions/nativeExtensions/LineHeight'
import AbstractExtension, { ActionType } from '~/components/common/editor/extensions/AbstractExtension'
import EditorTypography from '~/components/common/editor/EditorTypography.vue'
import HardBreak from '~/components/common/editor/extensions/nativeExtensions/HardBreak'
import Heading from '~/components/common/editor/extensions/nativeExtensions/Heading'
import TableOfContent from '~/components/common/editor/extensions/nativeExtensions/TableOfContent'
import Iframe from '~/components/common/editor/extensions/nativeExtensions/Iframe'
import Underline from '~/components/common/editor/extensions/nativeExtensions/Underline'
import FontColor from '~/components/common/editor/extensions/nativeExtensions/FontColor'

export default defineComponent({
  components: { EditorContent, BubbleMenu, EditorTypography },
  model: { prop: 'text', event: 'update' },
  props: {
    text: { type: String, default: () => ('') },
    extensions: {
      type: Array as PropType<AbstractExtension[]>,
      required: false,
      default: () => ([
        new Bold(),
        new Italic(),
        new Strike(),
        new Underline(),
        new Heading({ levels: [1, 2, 3] }),
        new TextAlign({ types: ['paragraph', 'heading'] }),
        new Image({ inline: true }),
        new File({ openOnClick: false }),
        new Link({ openOnClick: false }),
        new OrderedList(),
        new BulletList(),
        new Highlight({ multicolor: true }),
        new Table({ table: { resizable: true } }),
        new LineHeight(),
        new HTML(),
        new HardBreak(),
        new TableOfContent(),
        new Iframe(),
        new FontColor()
      ])
    }
  },
  setup (props, { emit }) {
    const editor = ref<CoreEditor>(null)
    const toolbarActions = ref<ActionType[]>([])
    const bubbleActions = ref<ActionType[]>([])
    const preview = ref(false)
    const isFullscreen = ref(false)

    const onUpdate = (props: { editor: CoreEditor }) => {
      emit('update', props.editor.getHTML())
    }
    const toggleFullscreen = () => {
      isFullscreen.value = !isFullscreen.value
    }

    onMounted(() => {
      const exts: any[] = []
      props.extensions.forEach((el: AbstractExtension) => {
        exts.push(el.nativeExtension)
        toolbarActions.value.push(...el.toolbarActions)
        bubbleActions.value.push(...el.bubbleActions)
      })
      editor.value = new Editor({
        content: props.text,
        extensions: [
          Document,
          Text,
          Paragraph,
          History,
          Gapcursor,
          Dropcursor,
          ListItem,
          TextStyle,
          ...exts
        ],
        onUpdate,
        autofocus: true
      })
    })
    onBeforeUnmount(() => {
      editor.value?.destroy()
    })
    return { isFullscreen, preview, toolbarActions, bubbleActions, editor, toggleFullscreen }
  }
})
</script>

<style lang="sass">
  .fullscreen
    border-radius: 0
    bottom: 0
    height: 100%
    left: 0
    margin: 0
    position: fixed
    right: 0
    top: 0
    width: 100%
    z-index: 500
  .editor_content
    min-height: 300px
    max-height: calc(100vh - 374px)
    overflow-y: auto
    flex-grow: 1
    .ProseMirror
      padding: 2px
      margin: 3px
      outline: 1px solid #555
      .focus
        outline: inherit
</style>
