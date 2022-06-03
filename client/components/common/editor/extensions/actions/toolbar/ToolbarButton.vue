<template lang="pug">
  v-tooltip(v-if="isVisible(editor)" top)
    template(#activator="{ on }")
      v-btn(v-on="on" :disabled="isDisabled(editor)" :class="{ 'v-btn--active': isActive(editor) }" @click="onClick(editor)" icon)
        v-icon {{icon}}
    span {{$t(`common.richTextEditor.${tooltip}`)}}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
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
  }
})
</script>
