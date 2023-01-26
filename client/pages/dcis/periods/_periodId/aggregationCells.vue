<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.aggregationCells.name') }}
    template(v-if="period.canChangeSettings")
  template(#subheader) {{ $t('shownOf', { count, totalCount: count }) }}
  v-data-table(
    :headers="tableHeaders"
    :items="aggregationCells"
    :loading="aggregationCellsLoading"
    disable-pagination
    hide-default-footer
  )
    template(#item.cells="{ item }")
      span(v-if="item.cells.length === 0") &mdash;
      strong(v-else) {{ item.cells.join(', ') }}
    template(#item.actions="{ item }")
      delete-menu(
        :item-name="String($t('dcis.periods.limitations.deleteItemName'))"
        @confirm="deleteLimitation({ limitationId: item.id })"
      )
        template(#default="{ on: onMenu }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip, attrs }")
              v-btn.ml-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" icon, color="error")
                v-icon mdi-delete
            span {{ String($t('dcis.periods.limitations.tooltips.delete')) }}

</template>

<script lang="ts">

import { computed, defineComponent, useNuxt2Meta } from '#app'
import type { PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  AggregationCellsQuery,
  AggregationCellsQueryVariables
} from '~/types/graphql'
import { useI18n, useCommonQuery } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import aggregationCellsQuery from '~/gql/dcis/queries/aggregation_cells.graphql'

export default defineComponent({
  components: { DeleteMenu, LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.aggregationCells.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-aggregationCells' }),
        exact: true
      }
    ]))

    const tableHeaders = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = [
        { text: t('dcis.periods.aggregationCells.tableHeaders.position') as string, value: 'position' },
        { text: t('dcis.periods.aggregationCells.tableHeaders.aggregateType') as string, value: 'aggregation' },
        { text: t('dcis.periods.aggregationCells.tableHeaders.listAggregateCells') as string, value: 'cells' }
      ]
      if (props.period.canChangeSettings) {
        result.push({
          text: t('dcis.periods.aggregationCells.tableHeaders.actions') as string,
          value: 'actions',
          align: 'center',
          sortable: false
        })
      }
      return result
    })

    const {
      data: aggregationCells,
      loading: aggregationCellsLoading,
      resetUpdate: aggregationCellsResetUpdate,
      addUpdate: aggregationCellsAddUpdate,
      deleteUpdate: aggregationCellsDeleteUpdate
    } = useCommonQuery<AggregationCellsQuery, AggregationCellsQueryVariables>({
      document: aggregationCellsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })
    const count = computed<number>(() => aggregationCells.value ? aggregationCells.value.length : 0)
    return {
      bc,
      tableHeaders,
      aggregationCells,
      aggregationCellsLoading,
      aggregationCellsResetUpdate,
      aggregationCellsAddUpdate,
      aggregationCellsDeleteUpdate,
      count
    }
  }
})
</script>
