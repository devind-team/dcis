<template lang="pug">
items-data-filter(
  v-model="selectedDivisions"
  :title="getFilterTitle"
  :items="divisionsItems"
  :message-function="getFilterMessageFunction"
  :get-name="item => item.name"
  :message-container-class="messageContainerClass"
  :search-function="filterSearchFunction"
  multiple
  modal
  fullscreen
)
  template(#items="{ searchItems, tempItems, setSelected, setAllSelected }")
    v-data-table(
    :value="tempItems"
    :headers="divisionsFilterTableHeaders"
    :items="organizationsItems || departmentItems"
    :show-select="!divisionSelection"
    disable-pagination
    hide-default-footer
    @item-selected="setSelected($event.item, $event.value)"
    @toggle-select-all="setAllSelected($event.value)"
  )
    pre {{ divisionsItems }}
    pre {{ organizationsItems || departmentItems }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import { useCommonQuery, useI18n } from '~/composables'
import { Class } from '~/types/filters'
import {
  PeriodType,
  DepartmentType,
  OrganizationType,
  PeriodFilterDepartmentsQuery,
  PeriodFilterOrganizationsQuery,
  PeriodFilterDepartmentsQueryVariables,
  PeriodFilterOrganizationsQueryVariables
} from '~/types/graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import periodFilterOrganizationsQuery from '~/gql/dcis/queries/period_filter_organizations.graphql'
import periodFilterDepartmentsQuery from '~/gql/dcis/queries/period_filter_departments.graphql'

type DivisionType = OrganizationType | DepartmentType

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<DivisionType[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const divisionSelection = ref<boolean>(false)

    const selectedDivisions = computed<DivisionType[]>({
      get () {
        return props.value
      },
      set (value: DivisionType[]) {
        emit('input', value)
      }
    })

    const getNameDivisions = computed(() => {
      return props.period.project.contentType.model === 'department'
        ? 'divisionFilterDepartment'
        : 'divisionFilterOrganization'
    })

    const getFilterTitle = t(`dcis.documents.${getNameDivisions.value}.title`) as string

    const getFilterMessageFunction = (selectedItems: []): string => {
      if (selectedItems.length === 0) {
        return t(`dcis.documents.${getNameDivisions.value}.noFiltrationMessage`) as string
      }
      return t(`dcis.documents.${getNameDivisions.value}.multipleMessage`, { count: selectedItems.length }) as string
    }

    const filterSearchFunction = (item, search: string): boolean => {
      return item.name.toLocaleLowerCase().includes(search.toLocaleLowerCase())
    }

    const divisionsFilterTableHeaders = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = []
      if (selectedDivisions.value) {
        result.push({ text: '', value: 'mainDocument', align: 'center', filterable: false, sortable: false })
      }
      if (props.period.project.contentType.model === 'department') {
        result.push(...[
          { text: t('dcis.documents.divisionFilterDepartment.tableHeaders.name') as string, value: 'name' },
          { text: t('dcis.documents.divisionFilterDepartment.tableHeaders.code') as string, value: 'code' }
        ])
      } else {
        result.push(...[
          { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.name') as string, value: 'name' },
          { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.kpp') as string, value: 'kpp' },
          { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.inn') as string, value: 'inn' },
          { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.kodbuhg') as string, value: 'kodbuhg' }
        ])
      }

      return result
    })

    const divisionsItems = computed(() => props.period.divisions)
    const { data: organizationsItems } = useCommonQuery<
      PeriodFilterOrganizationsQuery,
      PeriodFilterOrganizationsQueryVariables
    >({
      document: periodFilterOrganizationsQuery,
      variables: () => ({
        periodId: props.period.id
      }),
      options: computed(() => ({
        enabled: props.period.project.contentType.model === 'organization'
      }))
    })

    const { data: departmentItems } = useCommonQuery<
      PeriodFilterDepartmentsQuery,
      PeriodFilterDepartmentsQueryVariables
    >({
      document: periodFilterDepartmentsQuery,
      variables: () => ({
        periodId: props.period.id
      }),
      options: computed(() => ({
        enabled: props.period.project.contentType.model === 'department'
      }))
    })

    const divisionsItems1 = ref(organizationsItems || departmentItems)
    console.log(divisionsItems1)

    const active = ref<boolean>(false)
    const activeChanged = (value: boolean) => {
      active.value = value
    }

    return {
      divisionSelection,
      selectedDivisions,
      getNameDivisions,
      getFilterTitle,
      getFilterMessageFunction,
      filterSearchFunction,
      divisionsItems,
      divisionsFilterTableHeaders,
      organizationsItems,
      departmentItems,
      activeChanged
    }
  }
})
</script>
