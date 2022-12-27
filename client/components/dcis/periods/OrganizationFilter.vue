<template lang="pug">
items-data-filter(
  v-model="selectedOrganization"
  :title="title"
  :items="organizations || []"
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
import { computed, defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import { useCommonQuery, useI18n } from '~/composables'
import { Class } from '~/types/filters'
import {
  PeriodType,
  OrganizationType,
  PeriodFilterOrganizationsQuery,
  PeriodFilterOrganizationsQueryVariables
} from '~/types/graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import periodFilterOrganizationsQuery from '~/gql/dcis/queries/period_filter_organizations.graphql'

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<OrganizationType[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    title: { type: String, required: true },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const selectedOrganization = computed<OrganizationType[]>({
      get () {
        return props.value
      },
      set (value: OrganizationType[]) {
        emit('input', value)
      }
    })

    const getFilterMessageFunction = (selectedItems: []): string => {
      if (selectedItems.length === 0) {
        return t('dcis.documents.divisionFilterOrganization.noFiltrationMessage') as string
      }
      return t('dcis.documents.divisionFilterOrganization.multipleMessage', { count: selectedItems.length }) as string
    }

    const filterSearchFunction = (item: OrganizationType, search: string): boolean => {
      const searchLower = search.toLocaleLowerCase()
      let result = item.name.toLocaleLowerCase().includes(searchLower)
      if (item.kpp) {
        result = result || item.kpp.toLocaleLowerCase().includes(searchLower)
      }
      if (item.inn) {
        result = result || item.inn.toLocaleLowerCase().includes(searchLower)
      }
      if (item.kodbuhg) {
        result = result || item.kodbuhg.toLocaleLowerCase().includes(searchLower)
      }
      return result
    }

    const tableHeaders = computed<DataTableHeader[]>(() => [
      { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.kpp') as string, value: 'kpp' },
      { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.inn') as string, value: 'inn' },
      { text: t('dcis.documents.divisionFilterOrganization.tableHeaders.kodbuhg') as string, value: 'kodbuhg' }
    ])

    const { data: organizations } = useCommonQuery<
      PeriodFilterOrganizationsQuery,
      PeriodFilterOrganizationsQueryVariables
    >({
      document: periodFilterOrganizationsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    const active = ref<boolean>(false)
    const activeChanged = (value: boolean) => {
      active.value = value
    }

    return {
      selectedOrganization,
      getFilterMessageFunction,
      filterSearchFunction,
      tableHeaders,
      organizations,
      activeChanged
    }
  }
})
</script>
