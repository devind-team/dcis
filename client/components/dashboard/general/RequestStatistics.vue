<template lang="pug">
v-row(v-if="!loading")
  v-col(v-for="chart in charts" :key="chart" cols="12" sm="4")
    .caption {{ labels[chart] }}
    client-only
      apex-chart(
        type="donut"
        :options="statistics[chart].options"
        :series="statistics[chart].series")
</template>

<script lang="ts">
import { computed, defineComponent } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { RequestStatisticsQuery, RequestStatisticsQueryVariables, RequestStatisticsType } from '~/types/graphql'
import requestStatisticsQuery from '~/gql/dashboard/queries/request_statistics.graphql'

export default defineComponent({
  setup () {
    const { t } = useI18n()
    const charts: string[] = ['browsers', 'os', 'device']
    const labels = computed<Record<string, string>>(() => ({
      browsers: t('dashboard.general.requestStatistics.browsers') as string,
      os: t('dashboard.general.requestStatistics.os') as string,
      device: t('dashboard.general.requestStatistics.device') as string
    }))

    const { data: requestStatistics, loading } = useCommonQuery<RequestStatisticsQuery, RequestStatisticsQueryVariables>({
      document: requestStatisticsQuery
    })
    const getChartOptions = (rs: RequestStatisticsType, c: string) => ({
      options: { labels: rs[c].map(s => s.name) },
      series: rs[c].map(s => s.value)
    })
    const statistics = computed(() => (charts.reduce((a, c) => ({ ...a, [c]: getChartOptions(requestStatistics.value, c) }), {})))

    return { charts, labels, loading, statistics }
  }
})
</script>
