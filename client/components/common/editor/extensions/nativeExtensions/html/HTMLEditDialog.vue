<template lang="pug">
v-dialog(v-model="isDialog")
  template(#activator="{ on }")
    v-tooltip(top)
      template(#activator="{ on: onTooltip, attrs }")
        v-btn(v-on="{ ...on, ...onTooltip }" v-bind="attrs" icon)
          v-icon {{icon}}
      span {{$t(`common.richTextEditor.html.${tooltip}`)}}
  form(@submit.prevent="onInsert")
    v-card
      v-card-title {{$t(`common.richTextEditor.html.${tooltip}`)}}
        v-spacer
        v-btn(@click="isDialog=false" icon)
          v-icon mdi-close
      v-card-text
        v-textarea(v-model="content" auto-grow)
      v-card-actions
        v-spacer
        v-btn(type="submit" color="primary") {{ $t(`common.richTextEditor.html.${tooltip}`) }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { Editor } from '@tiptap/core'
import { OnButtonStateChangedType, OnClickType } from '~/components/common/editor/extensions/ExtensionOptionsInterface'

export default defineComponent({
  props: {
    tooltip: { type: String, required: true },
    icon: { type: String, required: true },
    editor: { type: Object as PropType<Editor>, required: true },
    onClick: { type: Function as PropType<OnClickType>, default: () => null },
    isDisabled: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isActive: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isVisible: { type: Function as PropType<OnButtonStateChangedType>, default: () => null }
  },
  setup (props) {
    const content = ref(props.editor.getHTML())
    const isDialog = ref(false)
    const onInsert = () => {
      props.onClick(props.editor, content.value)
      isDialog.value = false
    }
    return { content, isDialog, onInsert }
  }
})
</script>
