<template lang="pug">
left-navigator-container(
  :bread-crumbs="breadCrumbs"
  @update-drawer="$emit('update-drawer')"
)
  template(#header) {{ $t('dcis.periods.name') }}
    template(v-if="project.canAddPeriod")
      v-spacer
      add-period(
        :update="(cache, result) => addUpdate(cache, result, 'period')"
        :project="project"
      )
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ $t('dcis.periods.addPeriod.buttonText') }}
  template(#subheader)
    template(v-if="periods") {{ $t('shownOf', { count: periods.length, totalCount: totalCount }) }}
  period-status-filter(v-model="selectedFilters")
  v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
  v-data-table(
    :headers="headers"
    :items="periods"
    :loading="loading"
    disable-pagination
    hide-default-footer
  )
    template(#item.name="{ item }")
      nuxt-link(
        :to="localePath({ name: 'dcis-periods-periodId-documents', params: { periodId: item.id } })"
      ) {{ item.name }}
    template(#item.status="{ item }") {{ statuses[item.status] }}
    template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { computed, defineComponent, onMounted, ref } from '#app'
import { useRoute, useRouter } from '#imports'
import {
  useApolloHelpers,
  useCursorPagination,
  useDebounceSearch,
  useFilters,
  useI18n,
  useQueryRelay
} from '~/composables'
import { PeriodsQuery, PeriodsQueryVariables, PeriodType, ProjectType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'
import AddPeriod from '~/components/dcis/projects/AddPeriod.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import PeriodStatusFilter from '~/components/dcis/periods/PeriodStatusFilter.vue'
import { Item } from '~/types/filters'

export default defineComponent({
  name: 'ProjectPeriods',
  components: { LeftNavigatorContainer, AddPeriod, PeriodStatusFilter },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup () {
    const { t } = useI18n()
    const router = useRouter()
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    const { localePath } = useI18n()
    const { defaultClient } = useApolloHelpers()

    const { search, debounceSearch } = useDebounceSearch()
    const selectedFilters = ref<Item[]>([] || null)

    const statuses = Object.fromEntries(
      ['preparation', 'open', 'close'].map(e => ([e, t(`dcis.periods.statuses.${e}`) as string]))
    )
    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.periods.tableHeaders.status') as string, value: 'status' },
      { text: t('dcis.periods.tableHeaders.createdAt') as string, value: 'createdAt' }
    ]
    const periodQueryEnabled = ref<boolean>(false)
    const {
      data: periods,
      pagination: { count, totalCount },
      loading,
      addUpdate,
      deleteUpdate
    } = useQueryRelay<PeriodsQuery, PeriodsQueryVariables, PeriodType>({
      document: periodsQuery,
      variables: () => {
        return {
          projectId: route.params.projectId,
          statusFilter: selectedFilters.value.length ? selectedFilters.value[0].id : null,
          search: debounceSearch.value
        }
      },
      options: computed(() => ({
        enabled: periodQueryEnabled.value
      }))
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    onMounted(() => {
      periodQueryEnabled.value = true
      if (route.query.deletePeriodId) {
        deleteUpdate(
          defaultClient.cache,
          { data: { deletePeriod: { id: route.query.deletePeriodId } } },
          false
        )
        router.push(localePath({ name: 'dcis-projects-projectId-periods', params: route.params }))
      }
    })

    return {
      headers,
      periods,
      loading,
      count,
      totalCount,
      search,
      selectedFilters,
      addUpdate,
      dateTimeHM,
      statuses
    }
  }
})
</script>
