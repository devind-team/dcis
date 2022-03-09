<template lang="pug">
  v-row(v-if="!$apollo.queries.requestStatistics.loading")
    v-col(v-for="chart in charts" :key="chart" cols="12" sm="4")
      .caption {{ labels[chart] }}
      client-only
        apex-chart(
          type="donut"
          :options="statistics[chart].options"
          :series="statistics[chart].series")
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { RequestStatisticsType } from '~/types/graphql'

@Component<RequestStatistics>({
  apollo: {
    requestStatistics: {
      query: require('~/gql/dashboard/queries/request_statistics.graphql')
    }
  },
  computed: {
    charts (): string[] {
      return ['browsers', 'os', 'device']
    },
    labels (): { [key: string]: string } {
      return {
        browsers: this.t('browsers'),
        os: this.t('os'),
        device: this.t('device')
      }
    },
    // TODO: Нужно убрать эти any
    statistics (): any {
      return this.charts.reduce((a: any, c: any) => {
        return Object.assign(a, {
          [c]: {
            options: {
              labels: (this.requestStatistics as any)[c].map((s: any) => s.name)
            },
            series: (this.requestStatistics as any)[c].map((s: any) => s.value)
          }
        })
      }, {})
    }
  }
})
export default class RequestStatistics extends Vue {
  readonly requestStatistics!: RequestStatisticsType
  readonly charts!: string[]
  readonly label!: { [key: string]: string }
  readonly statistics!: { [key: string]: any }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`dashboard.general.requestStatistics.${path}`, values) as string
  }
}
</script>
