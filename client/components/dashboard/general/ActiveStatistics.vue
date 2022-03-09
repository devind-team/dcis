<template lang="pug">
  v-row(v-if="!loading")
    v-col(cols="12" sm="12")
      client-only
        apex-chart(type="area" height="450" :options="settings.options" :series="settings.series")
</template>

<script lang="ts">
import type { ComputedRef } from '#app'
import { computed, defineComponent } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { ActiveStatisticsQuery, ActiveStatisticsQueryVariables } from '~/types/graphql'
import activeStatisticsQuery from '~/gql/dashboard/queries/active_statistics.graphql'

export default defineComponent({
  setup () {
    const { t } = useI18n()
    const { data: as, loading } = useCommonQuery<ActiveStatisticsQuery, ActiveStatisticsQueryVariables>({ document: activeStatisticsQuery })
    const settings: ComputedRef = computed<any>(() => ({
      options: {
        xaxis: {
          type: 'datetime',
          categories: as.value.queries.map((e: any) => e.date)
        },
        yaxis: [
          { title: { text: t('dashboard.general.activeStatistics.numberOfRequests') } },
          { title: { text: t('dashboard.general.activeStatistics.seconds') }, opposite: true }
        ],
        dataLabels: {
          enabled: true,
          enabledOnSeries: [0]
        },
        chart: {
          toolbar: { show: false }
        }
      },
      series: [
        {
          name: t('dashboard.general.activeStatistics.userActivity'),
          type: 'line',
          data: as.value.queries.map((e: any) => Math.round(e.value))
        },
        {
          name: t('dashboard.general.activeStatistics.serverUptime'),
          type: 'column',
          data: as.value.times.map((e: any) => e.value.toFixed(4))
        }
      ]
    }))
    return { settings, loading }
  }
})
</script>
