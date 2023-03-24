<template lang="pug">
items-data-filter(
  v-model="selectedFilters"
  :title="String($t('dcis.projects.filter.title'))"
  :items="items"
  :get-name="i => String($t(`dcis.projects.filter.${i.id}`))"
  :no-filtration-message="String($t('dcis.projects.filter.noFiltrationMessage'))"
  :message-function="messageFunction"
  :default-value="defaultValue"
  multiple
)
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from '#app'
import { useI18n } from '~/composables'
import { GetName, Item } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<Item[]>, required: true },
    defaultValue: { type: Array as PropType<Item[]>, required: true }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const selectedFilters = computed<Item[]>({
      get () {
        return props.value
      },
      set (value: Item[]) {
        emit('input', value)
      }
    })

    const items: Item[] = [
      { id: 'active' },
      { id: 'hidden' },
      { id: 'archive' },
      { id: 'notArchive' }
    ]

    const messageFunction = (selectedItems: Item[], getName: GetName) => {
      if (selectedItems.length) {
        return selectedItems.map(getName).join(', ')
      } else {
        return String(t('dcis.projects.filter.noFiltrationMessage'))
      }
    }

    return { items, selectedFilters, messageFunction }
  }
})
</script>
