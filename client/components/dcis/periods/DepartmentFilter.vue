<template lang="pug">
items-data-filter(
  v-model="selectedDepartament"
  :title="title"
  :items="departments || []"
  :message-function="getFilterMessageFunction"
  :message-container-class="messageContainerClass"
  :search-function="filterSearchFunction"
  multiple
  modal
  fullscreen
)
  template(#items="{ searchItems, tempItems, setSelected, setAllSelected }")
    v-data-table(
      :value="tempItems"
      :headers="tableHeaders"
      :items="searchItems"
      disable-pagination
      hide-default-footer
      show-select
      @item-selected="setSelected($event.item, $event.value)"
      @toggle-select-all="setAllSelected($event.value)"
    )
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { useCommonQuery, useI18n } from '~/composables'
import { Class } from '~~/types/filters'
import {
  DepartmentType,
  PeriodType,
  PeriodFilterDepartmentsQuery,
  PeriodFilterDepartmentsQueryVariables
} from '~/types/graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import periodFilterDepartmentsQuery from '~/gql/dcis/queries/period_filter_departments.graphql'

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<DepartmentType[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    title: { type: String, required: true },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const selectedDepartament = computed<DepartmentType[]>({
      get () {
        return props.value
      },
      set (value: DepartmentType[]) {
        emit('input', value)
      }
    })

    const getFilterMessageFunction = (selectedItems: []): string => {
      if (selectedItems.length === 0) {
        return t('dcis.periods.departmentFilter.noFiltrationMessage') as string
      }
      return t('dcis.periods.departmentFilter.multipleMessage', { count: selectedItems.length }) as string
    }

    const filterSearchFunction = (item: DepartmentType, search: string): boolean => {
      const searchLower = search.toLocaleLowerCase()
      let result = item.name.toLocaleLowerCase().includes(searchLower)
      if (item.code) {
        result = result || String(item.code).toLocaleLowerCase().includes(searchLower)
      }
      return result
    }

    const tableHeaders = computed<DataTableHeader[]>(() => [
      { text: t('dcis.periods.departmentFilter.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.periods.departmentFilter.tableHeaders.code') as string, value: 'code' }
    ])

    const { data: departments } = useCommonQuery<
      PeriodFilterDepartmentsQuery,
      PeriodFilterDepartmentsQueryVariables
    >({
      document: periodFilterDepartmentsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    return {
      selectedDepartament,
      getFilterMessageFunction,
      filterSearchFunction,
      tableHeaders,
      departments
    }
  }
})

</script>
