<template lang="pug">
left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
  template(#header) {{ t('dcis.periods.name') }}
    template(v-if="project.canAddPeriod")
      v-spacer
      add-period(:update="addPeriodUpdate" :project="project")
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ t('dcis.periods.addPeriod.buttonText') }}
  template(#subheader)
    template(v-if="periods") {{ $t('shownOf', { count: periods.length, totalCount: periods.length }) }}
  v-data-table(:headers="headers" :items="periods" :loading="loading" disable-pagination hide-default-footer)
    template(#item.name="{ item }")
      nuxt-link(
        :to="localePath({ name: 'dcis-periods-periodId-documents', params: { periodId: toGlobalId('PeriodType', item.id) } })"
      ) {{ item.name }}
    template(#item.status="{ item }") {{ statuses[item.status] }}
    template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { defineComponent, onMounted } from '#app'
import { useRoute, useRouter } from '#imports'
import { useApolloHelpers, useCommonQuery, useFilters, useI18n } from '~/composables'
import { PeriodsQuery, PeriodsQueryVariables, ProjectType } from '~/types/graphql'
import { toGlobalId } from '~/services/graphql-relay'
import { BreadCrumbsItem } from '~/types/devind'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'
import AddPeriod, { AddPeriodMutationResult } from '~/components/dcis/projects/AddPeriod.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  name: 'ProjectPeriods',
  components: { LeftNavigatorContainer, AddPeriod },
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

    const statuses = Object.fromEntries(
      ['preparation', 'open', 'close'].map(e => ([e, t(`dcis.periods.statuses.${e}`) as string]))
    )
    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.periods.tableHeaders.status') as string, value: 'status' },
      { text: t('dcis.periods.tableHeaders.createdAt') as string, value: 'createdAt' }
    ]
    const {
      data: periods,
      loading,
      addUpdate,
      update
    } = useCommonQuery<PeriodsQuery, PeriodsQueryVariables>({
      document: periodsQuery,
      variables: { projectId: route.params.projectId }
    })

    const addPeriodUpdate = (
      cache: DataProxy,
      result: AddPeriodMutationResult
    ) => addUpdate(cache, result, 'period')

    onMounted(() => {
      if (route.query.deletePeriodId) {
        update(
          defaultClient.cache,
          { data: { deletePeriod: { id: route.query.deletePeriodId } } },
          (cacheData, { data: { deletePeriod: { id: periodId } } }
          ) => {
            cacheData.periods = cacheData.periods.filter(period => period.id !== periodId)
            return cacheData
          })
        router.push(localePath({ name: 'dcis-projects-projectId-periods', params: route.params }))
      }
    })

    return { t, headers, periods, loading, addPeriodUpdate, dateTimeHM, toGlobalId, statuses }
  }
})
</script>
