<template lang="pug">
  v-dialog(v-if="isVisible(editor)" v-model="isDialog" width="600")
    template(#activator="{ on }")
      v-tooltip(top)
        template(#activator="{ on: onTooltip, attrs }")
          v-btn(v-on="{ ...on, ...onTooltip }" v-bind="attrs" icon @click="onOpen")
            v-icon {{icon}}
        span {{$t('common.richTextEditor.image.changeImage')}}
    validation-observer(v-slot="{ invalid }")
      form(@submit.prevent="onDone")
        v-card
          v-card-title {{$t('common.richTextEditor.image.changeImage')}}
            v-spacer
            v-btn(@click="isDialog=false" icon)
              v-icon mdi-close
          v-card-text
            v-select(v-model="sizeMode" :items="sizeModes")
            validation-provider(:name="$t('common.richTextEditor.image.width')" rules="required|min_value:1" v-slot="{ errors, valid }")
              v-text-field(v-model="width" :label="$t('common.richTextEditor.image.width')" type="number" :error-messages="errors" :success="valid")
            v-btn(:class="{ 'v-btn--active': keepAspectRatio }" @click="onAspectRatioChanged" icon)
              v-icon mdi-link
            validation-provider(:name="$t('common.richTextEditor.image.height')" rules="required|min_value:1" v-slot="{ errors, valid }")
              v-text-field(v-model="height" :label="$t('common.richTextEditor.image.height')" type="number" :disabled="keepAspectRatio" :error-messages="errors" :success="valid")
          v-card-actions
            v-spacer
            v-btn(type="submit" :disabled="invalid" color="primary") {{ $t('common.richTextEditor.image.changeImage') }}
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
    const sizeModes = computed(() => {
      return [
        { text: t('common.richTextEditor.image.px'), value: 'px' },
        { text: t('common.richTextEditor.image.pc'), value: '%' }
      ]
    })
    const isDialog = ref(false)
    const keepAspectRatio = ref(false)
    const height = ref(0)
    const width = ref(0)
    const sizeMode = ref('px')
    const onOpen = () => {
      const from = props.editor.state.selection.from
      const to = props.editor.state.selection.to
      props.editor.state.doc.nodesBetween(from, to, (node: any) => {
        if (node.type.name === 'image') {
          height.value = node.attrs.height.toFixed()
          width.value = node.attrs.width.toFixed()
          sizeMode.value = node.attrs.sizeMode
          keepAspectRatio.value = node.attrs.keepAspectRatio
        }
      })
    }
    const onAspectRatioChanged = () => {
      keepAspectRatio.value = !keepAspectRatio.value
    }
    const onDone = () => {
      props.editor.chain().focus().updateAttributes('image', { width: width.value, height: height.value, keepAspectRatio: keepAspectRatio.value, sizeMode: sizeMode.value }).run()
      isDialog.value = false
    }
    return { isDialog, keepAspectRatio, height, width, sizeMode, sizeModes, onOpen, onAspectRatioChanged, onDone }
  }
})
</script>
