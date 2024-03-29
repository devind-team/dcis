<template lang="pug">
items-data-filter(
  v-model="selectedOrganization"
  :title="title"
  :items="changeOrganizations || []"
  :message-function="filterMessageFunction"
  :message-container-class="messageContainerClass"
  :search-function="filterSearchFunction"
  multiple
  modal
  fullscreen
)
  template(#subtitle) {{ $t('shownOf', { count, totalCount: totalCount }) }}
  template(#filter)
    v-card-text(style="flex: none")
      organization-level-filter(v-model="selectedFilters")
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
import { fromGlobalId } from '~/services/graphql-relay'
import { useQueryRelay, useI18n, useCursorPagination } from '~/composables'
import { Class, Item } from '~/types/filters'
import {
  PeriodType,
  OrganizationType,
  PeriodFilterOrganizationsQuery,
  PeriodFilterOrganizationsQueryVariables
} from '~/types/graphql'
import periodFilterOrganizationsQuery from '~/gql/dcis/queries/period_filter_organizations.graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import OrganizationLevelFilter from '~/components/dcis/periods/OrganizationLevelFilter.vue'

export default defineComponent({
  components: { ItemsDataFilter, OrganizationLevelFilter },
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

    const filterMessageFunction = (selectedItems: []): string => {
      if (selectedItems.length === 0) {
        return t('dcis.periods.organizationFilter.noFiltrationMessage') as string
      }
      return t('dcis.periods.organizationFilter.multipleMessage', { count: selectedItems.length }) as string
    }

    const filterSearchFunction = (item: OrganizationType, search: string): boolean => {
      const searchLower = search.toLocaleLowerCase()
      let result = item.id.toLocaleLowerCase().includes(searchLower)
      if (item.name) {
        result = result || item.name.toLocaleLowerCase().includes(searchLower)
      }
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
    const selectedFilters = ref<Item[]>([] || null)
    const tableHeaders = computed<DataTableHeader[]>(() => [
      { text: t('dcis.periods.organizationFilter.tableHeaders.id') as string, value: 'id' },
      { text: t('dcis.periods.organizationFilter.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.periods.organizationFilter.tableHeaders.kpp') as string, value: 'kpp' },
      { text: t('dcis.periods.organizationFilter.tableHeaders.inn') as string, value: 'inn' },
      { text: t('dcis.periods.organizationFilter.tableHeaders.kodbuhg') as string, value: 'kodbuhg' }
    ])

    const {
      data: organizations,
      pagination: { count, totalCount }
    } = useQueryRelay<
      PeriodFilterOrganizationsQuery,
      PeriodFilterOrganizationsQueryVariables,
      OrganizationType
    >({
      document: periodFilterOrganizationsQuery,
      variables: () => ({
        periodId: props.period.id,
        attributesLevel: selectedFilters.value.length ? String(t(`dcis.periods.organizationFilter.levelFilter.types.${selectedFilters.value[0].id}`)) : null
      })
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    const changeOrganizations = computed(() => {
      if (!organizations.value) {
        return []
      }
      return organizations.value.map(organization => ({
        ...organization,
        id: String(fromGlobalId(organization.id).id)
      })
      )
    })

    return {
      selectedOrganization,
      filterMessageFunction,
      filterSearchFunction,
      selectedFilters,
      tableHeaders,
      count,
      totalCount,
      changeOrganizations
    }
  }
})
</script>
