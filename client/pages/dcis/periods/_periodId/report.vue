<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.report.name') }}
    v-spacer
    report-settings-menu(v-slot="{ on, attrs }")
      v-btn(v-on="on" v-bind="attrs" icon)
        v-icon mdi-cog
  report-document-filter(
    v-model="reportDocumentFilterData"
    :period="period"
    message-container-class="mb-2 mr-1"
  )
  items-data-filter(
    v-model="reportRows"
    ref="reportRowsFilter"
    :items="reportRowsItems"
    :title="String($t('dcis.periods.report.rowsFilter.title'))"
    :message-function="reportRowsMessageFunction"
    :search-function="reportRowsSearchFunction"
    :get-name="item => item.name"
    item-key="name"
    message-container-class="mb-2"
    multiple
  )
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.READ"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
    :loading="activeSheetLoading"
  )
</template>

<script lang="ts">
import { computed, defineComponent, ref, PropType, inject, watch } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { positionsToRangeIndices } from '~/services/grid'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, BaseSheetType, ReportSheetQuery, ReportSheetQueryVariables } from '~/types/graphql'
import reportSheetQuery from '~/gql/dcis/queries/report_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ReportSettingsMenu from '~/components/dcis/periods/ReportSettingsMenu.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import ReportDocumentFilter, {
  ReportDocumentType,
  ReportDocumentFilterInputType
} from '~/components/dcis/periods/ReportDocumentFilter.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

type ReportRow = { indices: number[], name: string }

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    ReportSettingsMenu,
    GridSheets,
    ReportDocumentFilter,
    ItemsDataFilter
  },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.report.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-report' }),
        exact: true
      }
    ]))

    const activeSheetIndex = ref<number>(0)
    const activeBaseSheet = computed<BaseSheetType>(() => props.period.sheets[activeSheetIndex.value])

    const reportDocumentFilterData = ref<ReportDocumentFilterInputType>({
      reportDocuments: [],
      mainDocument: null,
      aggregation: null
    })

    const reportRowsFilter = ref<InstanceType<typeof ItemsDataFilter>>(null)
    const reportRows = ref<ReportRow[]>([])
    const reportRowsItems = computed<ReportRow[]>(() => {
      if (!activeSheet.value) {
        return []
      }
      const result: ReportRow[] = []
      let i = 0
      while (i < activeSheet.value.rows.length) {
        let max = 1
        for (const cell of activeSheet.value.rows[i].cells) {
          const { minRow, maxRow } = positionsToRangeIndices(cell.relatedGlobalPositions)
          const rowsCount = maxRow - minRow + 1
          if (rowsCount > max) {
            max = rowsCount
          }
        }
        const indices = Array.from({ length: max }).map((_, index) => i + index + 1)
        result.push({ indices, name: indices.join(', ') })
        i += max
      }
      return result
    })
    const reportRowsMessageFunction = (selectedItems: ReportRow[]): string => {
      if (selectedItems.length) {
        return t('dcis.periods.report.rowsFilter.multipleMessage', { count: selectedItems.length }) as string
      }
      return t('dcis.periods.report.rowsFilter.noFiltrationMessage') as string
    }
    const reportRowsSearchFunction = (item: ReportRow, search: string): boolean => {
      return item.name.toLocaleLowerCase().includes(search.toLocaleLowerCase())
    }
    watch(() => activeSheetIndex.value, () => {
      reportRowsFilter.value.reset()
    })

    const { data: activeSheet, loading: activeSheetLoading } = useCommonQuery<
      ReportSheetQuery,
      ReportSheetQueryVariables
    >({
      document: reportSheetQuery,
      variables: () => ({
        sheetId: activeBaseSheet.value.id,
        reportDocuments: reportDocumentFilterData.value.reportDocuments.map((rd: ReportDocumentType) => ({
          documentId: rd.document.id,
          isVisible: rd.isVisible,
          color: rd.color
        })),
        reportRows: Array.from({ length: activeBaseSheet.value.rowsCount }).map((_, i) => ({
          rowIndex: i + 1,
          isExpanded: !!reportRows.value.find((r: ReportRow) => r.indices.includes(i + 1))
        })),
        mainDocumentId: reportDocumentFilterData.value.mainDocument?.id,
        aggregation: reportDocumentFilterData.value.aggregation ?? null
      })
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      GridMode,
      bc,
      reportDocumentFilterData,
      reportRowsFilter,
      reportRows,
      reportRowsItems,
      reportRowsMessageFunction,
      reportRowsSearchFunction,
      activeSheetIndex,
      activeSheet,
      activeSheetLoading
    }
  }
})
</script>
