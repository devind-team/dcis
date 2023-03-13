<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.aggregationCells.name') }}
    template(v-if="period.canChangeSettings")
      v-spacer
      change-period-aggregation-cells-menu(
        :period="period"
        :from-file-update="aggregationsResetUpdate"
        :add-update="aggregationsAddUpdate"
      )
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.periods.aggregationCells.changeMenu.buttonText') }}
  template(#subheader) {{ $t('shownOf', { count, totalCount: count }) }}
  v-data-table(
    :headers="tableHeaders"
    :items="aggregations"
    :loading="aggregationsLoading"
    disable-pagination
    hide-default-footer
  )
    template(#item.cells="{ item }")
      strong(v-if="item.cells.length === 0") &mdash;
      span(v-else) {{ item.cells.join(', ') }}
    template(#item.aggregation="{ item }") {{ $t(`dcis.periods.aggregationCells.kinds.${item.aggregation}`) }}
    template(#item.actions="{ item }")
      delete-menu(
        :item-name="String($t('dcis.periods.aggregationCells.deleteItemName'))"
        @confirm="deleteAggregationCell({ aggregationCellId : item.id })"
      )
        template(#default="{ on: onMenu }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip, attrs }")
              v-btn.ml-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" icon, color="error")
                v-icon mdi-delete
            span {{ String($t('dcis.periods.aggregationCells.tooltips.delete')) }}
</template>

<script lang="ts">
import { computed, defineComponent, useNuxt2Meta } from '#app'
import type { PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  AggregationCellsQuery,
  AggregationCellsQueryVariables, DeleteAggregationMutationVariables, DeleteAggregationMutation
} from '~/types/graphql'
import { useI18n, useCommonQuery } from '~/composables'
import aggregationCellsQuery from '~/gql/dcis/queries/aggregation_cells.graphql'
import deleteAggregationMutation from '~/gql/dcis/mutations/aggregation/delete_aggregation.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import ChangePeriodAggregationCellsMenu from '~/components/dcis/periods/ChangePeriodAggregationCellsMenu.vue'

export default defineComponent({
  components: { ChangePeriodAggregationCellsMenu, DeleteMenu, LeftNavigatorContainer },
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
        to: localePath({ name: 'dcis-periods-periodId-aggregations' }),
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
      data: aggregations,
      loading: aggregationsLoading,
      resetUpdate: aggregationsResetUpdate,
      addUpdate: aggregationsAddUpdate,
      deleteUpdate: aggregationsDeleteUpdate
    } = useCommonQuery<
      AggregationCellsQuery,
      AggregationCellsQueryVariables
    >({
      document: aggregationCellsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })
    const count = computed<number>(() => aggregations.value ? aggregations.value.length : 0)

    const { mutate: deleteAggregationCell } = useMutation<
      DeleteAggregationMutation,
      DeleteAggregationMutationVariables
    >(deleteAggregationMutation, {
      update: (cache, result) => aggregationsDeleteUpdate(cache, result)
    })

    watch(aggregations, (new_value) => { console.log(new_value) })

    return {
      bc,
      tableHeaders,
      aggregations,
      aggregationsLoading,
      aggregationsResetUpdate,
      aggregationsAddUpdate,
      aggregationsDeleteUpdate,
      count,
      deleteAggregationCell
    }
  }
})
</script>
