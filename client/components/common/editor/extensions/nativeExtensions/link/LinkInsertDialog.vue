<template lang="pug">
v-dialog(v-model="isDialog" width="600")
  template(#activator="{ on }")
    v-tooltip(top)
      template(#activator="{ on: onTooltip, attrs }")
        v-btn(v-on="{ ...on, ...onTooltip }" v-bind="attrs" @click="initLabel" icon)
          v-icon {{icon}}
      span {{$t(`common.richTextEditor.link.${tooltip}`)}}
  validation-observer(v-slot="{ invalid }")
    form(@submit.prevent="onInsert")
      v-card
        v-card-title {{$t(`common.richTextEditor.link.${tooltip}`)}}
          v-spacer
          v-btn(@click="isDialog = false" icon)
            v-icon mdi-close
        v-card-text
          validation-provider(:name="$t('common.richTextEditor.link.src')" rules="required" v-slot="{ errors, valid }")
            v-text-field(
              :label="$t('common.richTextEditor.link.src')"
              :success="valid"
              :error-messages="errors"
              v-model="src"
              @input="onSrcInput")
          v-text-field(:label="$t('common.richTextEditor.link.label')" v-model="label" @change="onLabelInput")
          v-select(
            v-model="target"
            :label="$t('common.richTextEditor.link.openIn')"
            :items="targets"
            item-text="text"
            item-value="value"
            auto-select-first)
        v-card-actions
          v-spacer
          v-btn(type="submit" :disabled="invalid" color="primary") {{ $t(`common.richTextEditor.link.${tooltip}`) }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed } from '#app'
import { Editor } from '@tiptap/core'
import { useI18n } from '~/composables'
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
    const { t } = useI18n()

    const isMirroring = ref(true)
    const isDialog = ref(false)
    const src = ref('')
    const label = ref('')
    const target = ref('_blank')

    const targets = computed(() => {
      return [
        { text: t('common.richTextEditor.link.currentWindow'), value: '_self' },
        { text: t('common.richTextEditor.link.newWindow'), value: '_blank' }
      ]
    })

    const onInsert = () => {
      props.onClick(props.editor, { src: src.value, label: label.value, target: target.value })
      isDialog.value = false
      src.value = ''
      label.value = ''
      isMirroring.value = true
    }
    const onSrcInput = () => {
      if (isMirroring.value) {
        label.value = src.value
      }
    }
    const onLabelInput = (value: string) => {
      isMirroring.value = !value
      if (isMirroring.value) {
        label.value = src.value
      }
    }
    const initLabel = () => {
      if (props.editor.view.state.selection.empty) {
        return
      }
      const { state } = props.editor
      const selection = props.editor.view.state.selection
      const { from, to } = selection
      label.value = state.doc.textBetween(from, to, ' ')
      isMirroring.value = false
    }
    return { isDialog, label, target, targets, src, initLabel, onLabelInput, onSrcInput, onInsert }
  }
})
</script>
