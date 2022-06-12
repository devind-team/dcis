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
    const highlightColor = ref('#12345678')
    const defaultSwatches = ref([
      ['transparent', '#00FF00FF'],
      ['#FF0000FF', '#00FFFFFF'],
      ['#FFFF00FF', '#0000FFFF']
    ])
    const onColorChanged = (color: string) => {
      props.onClick(props.editor, color)
      highlightColor.value = '#12345678' // костыль
    }
    return { highlightColor, defaultSwatches, onColorChanged }
  }
})
</script>

<style lang="sass">
.swatches
  .v-icon
    display: none
</style>
