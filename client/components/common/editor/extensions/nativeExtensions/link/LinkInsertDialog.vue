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
    isMirroring: true,
    isDialog: false,
    src: '',
    label: '',
    target: '_blank'
  }),
  computed: {
    targets () {
      return [
        { text: this.$t('common.richTextEditor.link.currentWindow'), value: '_self' },
        { text: this.$t('common.richTextEditor.link.newWindow'), value: '_blank' }
      ]
    }
  },
  methods: {
    onInsert (): void {
      this.onClick(this.editor, { src: this.src, label: this.label, target: this.target })
      this.isDialog = false
      this.src = ''
      this.label = ''
      this.isMirroring = true
    },
    onSrcInput (): void {
      if (this.isMirroring) {
        this.label = this.src
      }
    },
    onLabelInput (value: string): void {
      this.isMirroring = !value
      if (this.isMirroring) {
        this.label = this.src
      }
    },
    initLabel (): void {
      if (this.editor.view.state.selection.empty) {
        return
      }
      const { state } = this.editor
      const selection = this.editor.view.state.selection
      const { from, to } = selection
      this.label = state.doc.textBetween(from, to, ' ')
      this.isMirroring = false
    }
  }
})
</script>
