<template lang="pug">
items-data-filter(
  v-model="selectedDivisions"
  v-bind="filterMessages"
  :items="period.divisions.map(d => ({ id: d.id, name: d.name }))"
  :get-name="d => d.name"
  :search-function="(d, s) => d.name.toLocaleLowerCase().includes(s.toLocaleLowerCase())"
  message-container-class="mr-1 mb-1"
  multiple
  has-select-all
)
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { useI18n } from '~/composables'
import { FilterMessages } from '~/types/filters'
import { DivisionModelType, PeriodType } from '~/types/graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<DivisionModelType[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props, { emit }) {
    const { t, tc } = useI18n()

    const selectedDivisions = computed<DivisionModelType[]>({
      get () {
        return props.value
      },
      set (value: DivisionModelType[]) {
        emit('input', value)
      }
    })

    const filterMessages = computed<FilterMessages>(() => {
      const filterName = props.period.project.contentType.model === 'department'
        ? 'divisionFilterDepartment'
        : 'divisionFilterOrganization'
      return getFilterMessages(filterName, true)
    })

    const getFilterMessages = (filterName: string, multiple: boolean = false): FilterMessages => {
      return {
        title: t(`dcis.documents.${filterName}.title`) as string,
        noFiltrationMessage: t(`dcis.documents.${filterName}.noFiltrationMessage`) as string,
        multipleMessageFunction: multiple
          ? (name, restLength) =>
              tc(`dcis.documents.${filterName}.multipleMessage`, restLength, { name, restLength }) as string
          : undefined
      }
    }

    return { selectedDivisions, filterMessages }
  }
})
</script>
