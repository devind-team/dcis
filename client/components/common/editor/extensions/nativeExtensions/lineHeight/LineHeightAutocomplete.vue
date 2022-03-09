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
import Vue, { PropType } from 'vue'
import { Editor } from '@tiptap/core'
import { OnButtonStateChangedType, OnClickType } from '~/components/common/editor/extensions/ExtensionOptionsInterface'

type ItemType = { text: string, value: string }

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
    item: null
  }),
  computed: {
    items (): ItemType[] {
      return [
        { text: this.$t('common.richTextEditor.lineHeight.default') as string, value: 'default' },
        { text: '1.0', value: '1.0' },
        { text: '1.15', value: '1.15' },
        { text: '1.5', value: '1.5' },
        { text: '2.0', value: '2.0' },
        { text: '2.5', value: '2.5' },
        { text: '3.0', value: '3.0' }
      ]
    }
  },
  methods: {
    onChange (value: number) {
      this.onClick(this.editor, this.items[value].value)
    }
  }
})
</script>
