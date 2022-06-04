<template lang="pug">
  v-menu(v-if="isVisible(editor)")
    template(#activator="{ on }")
      v-tooltip(v-if="isVisible(editor)" top)
        template(#activator="{ on: onTooltip }")
          v-btn(v-on="{...on, ...onTooltip}"
            :disabled="isDisabled(editor)"
            :class="{ 'v-btn--active': isActive(editor) }"
            @click="() => item = null"
            icon)
            v-icon {{icon}}
        span {{$t(`common.richTextEditor.${tooltip}`)}}
    v-card
      v-card-text
        v-list
          v-list-item-group(v-model="item" @change="onChange")
            v-list-item(v-for="item in items" :key="item.value")
              v-list-item-content
                v-list-item-title {{item.text}}
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed } from '#app'
import { Editor } from '@tiptap/core'
import { useI18n } from '~/composables'
import { OnButtonStateChangedType, OnClickType } from '~/components/common/editor/extensions/ExtensionOptionsInterface'

type ItemType = { text: string, value: string }

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
    const item = ref<ItemType>(null)

    const items = computed(() => {
      return [
        { text: t('common.richTextEditor.lineHeight.default') as string, value: 'default' },
        { text: '1.0', value: '1.0' },
        { text: '1.15', value: '1.15' },
        { text: '1.5', value: '1.5' },
        { text: '2.0', value: '2.0' },
        { text: '2.5', value: '2.5' },
        { text: '3.0', value: '3.0' }
      ]
    })
    const onChange = (value: number) => {
      props.onClick(props.editor, items.value[value].value)
    }
    return { item, items, onChange }
  }
})
</script>
