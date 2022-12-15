<template lang="pug">
items-data-filter(
  v-model="selectedFilters"
  :title="String($t('dcis.projects.filter.title'))"
  :items="items"
  :get-name="i => String($t(`dcis.projects.filter.${i.id}`))"
  :no-filtration-message="String($t('dcis.projects.filter.noFiltrationMessage'))"
  :default-value="defaultValue"
  multiple
)
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from '#app'
import { ProjectType } from '~/types/graphql'
import { Item } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<Item[]>, required: true },
    defaultValue: { type: Array as PropType<Item[]>, required: true },
    projects: { type: Array as PropType<ProjectType[]>, required: true }
  },
  setup (props, { emit }) {
    const selectedFilters = computed<Item[]>({
      get () {
        return props.value
      },
      set (value: Item[]) {
        emit('input', value)
      }
    })

    const items = computed<Item[]>(() => {
      const result: Item[] = [
        { id: 'active' },
        { id: 'archive' }
      ]
      if (props.projects.find(x => !x.visibility)) {
        result.push({ id: 'hidden' })
      }
      return result
    })

    return { items, selectedFilters }
  }
})
</script>
