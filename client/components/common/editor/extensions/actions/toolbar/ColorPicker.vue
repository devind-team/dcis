<template lang="pug">
  v-menu(v-if="isVisible(editor)")
    template(#activator="{ on }")
      v-tooltip(top)
        template(#activator="{ on: onTooltip }")
          v-btn(v-on="{ ...on, ...onTooltip }" :disabled="isDisabled(editor)" :class="{ 'v-btn--active': isActive(editor) }" icon)
            v-icon {{icon}}
        span {{$t(`common.richTextEditor.${tooltip}`)}}
    v-card
      v-card-text
        v-color-picker.swatches(
          v-model="highlightColor"
          :swatches="defaultSwatches"
          @input="onColorChanged"
          show-swatches
          hide-canvas
          hide-sliders
          hide-inputs
        )
</template>
<script lang="ts">
import Vue, { PropType } from 'vue'
import { Editor } from '@tiptap/core'
import { OnButtonStateChangedType, OnClickType } from '~/components/common/editor/extensions/ExtensionOptionsInterface'

export default Vue.extend<any, any, any, any>({
  props: {
    tooltip: { type: String, required: true },
    icon: { type: String, required: true },
    editor: { type: Object as PropType<Editor>, required: true },
    onClick: { type: Function as PropType<OnClickType>, default: () => null },
    isDisabled: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isActive: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isVisible: { type: Function as PropType<OnButtonStateChangedType>, default: () => null }
  },
  data: () => ({
    highlightColor: '#12345678',
    defaultSwatches: [
      ['transparent', '#00FF00FF'],
      ['#FF0000FF', '#00FFFFFF'],
      ['#FFFF00FF', '#0000FFFF']
    ]
  }),
  methods: {
    onColorChanged (color: string) {
      this.onClick(this.editor, color)
      this.highlightColor = '#12345678' // костыль
    }
  }
})
</script>

<style lang="sass">
.swatches
  .v-icon
    display: none
</style>
