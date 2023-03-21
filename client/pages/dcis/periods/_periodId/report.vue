<template lang="pug">
left-navigator-container.report-sheets__left-navigator-container(
  :bread-crumbs="bc"
  fluid
  @update-drawer="$emit('update-drawer')"
)
  template(#header) {{ $t('dcis.periods.report.name') }}
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.REPORT"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
    :loading="loading"
  )
    template(#menus="{ selectedCellsOptions }")
      edit-menu(:mode="GridMode.REPORT" :selected-cells-options="selectedCellsOptions")
      report-unload-menu
        template(#documents-filter="{ title }")
          report-document-filter(v-model="reportDocumentFilterData" :period="period")
            template(#message="{ on, attrs, disabled }")
              v-list-item(v-on="on" v-bind="attrs" :disabled="disabled")
                v-list-item-title {{ title }}
        template(#rows-filter="{ title }")
          items-data-filter(
            v-model="reportRowGroups"
            ref="reportRowGroupsFilter"
            :items="reportRowGroupsItems"
            :title="String($t('dcis.periods.report.rowsFilter.title'))"
            :disabled="!reportDocumentFilterData.reportDocuments.length"
            :search-function="reportRowGroupsSearchFunction"
            :get-name="item => item.name"
            item-key="name"
            message-container-class="mb-2"
            has-select-all
            multiple
          )
            template(#message="{ on, attrs, disabled }")
              v-list-item(v-on="on" v-bind="attrs" :disabled="disabled")
                v-list-item-title {{ title }}
</template>

<script lang="ts">
import { computed, defineComponent, ref, PropType, inject, watch } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  BaseSheetType,
  IndicesGroupsToExpandQuery,
  IndicesGroupsToExpandQueryVariables,
  ReportSheetQuery,
  ReportSheetQueryVariables
} from '~/types/graphql'
import indicesToExpandQuery from '~/gql/dcis/queries/indices_to_expand.graphql'
import reportSheetQuery from '~/gql/dcis/queries/report_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import EditMenu from '~/components/dcis/grid/menus/EditMenu.vue'
import ReportUnloadMenu from '~/components/dcis/grid/menus/ReportUnloadMenu.vue'
import ReportDocumentFilter, {
  ReportDocumentType,
  ReportDocumentFilterInputType
} from '~/components/dcis/periods/ReportDocumentFilter.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

type ReportRowGroup = { index: number, indices: number[], name: string }

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    GridSheets,
    EditMenu,
    ReportUnloadMenu,
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
    watch(() => reportDocumentFilterData.value, (newValue) => {
      if (!newValue.reportDocuments.length) {
        reportRowGroups.value = []
      }
    })

    const { data: indicesGroupsToExpand, loading: indicesGroupsToExpandLoading } = useCommonQuery<
      IndicesGroupsToExpandQuery,
      IndicesGroupsToExpandQueryVariables
    >({
      document: indicesToExpandQuery,
      variables: () => ({
        sheetId: activeBaseSheet.value.id
      })
    })
    const reportRowGroupsFilter = ref<InstanceType<typeof ItemsDataFilter>>(null)
    const reportRowGroups = ref<ReportRowGroup[]>([])
    const reportRowGroupsItems = computed<ReportRowGroup[]>(() => {
      if (!indicesGroupsToExpand.value) {
        return []
      }
      return indicesGroupsToExpand.value.map((indices: number[], index: number) => ({
        index,
        indices,
        name: indices.join(', ')
      }))
    })
    const reportRowGroupsSearchFunction = (item: ReportRowGroup, search: string): boolean => {
      return item.name.toLocaleLowerCase().includes(search.toLocaleLowerCase())
    }
    watch(() => activeSheetIndex.value, () => {
      if (reportRowGroupsFilter.value) {
        reportRowGroupsFilter.value.reset()
      }
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
        reportRowGroups: indicesGroupsToExpand.value
          ? Array.from({ length: indicesGroupsToExpand.value.length }).map((_, i) => ({
            groupIndex: i,
            isExpanded: !!reportRowGroups.value.find((r: ReportRowGroup) => r.index === i)
          }))
          : [],
        mainDocumentId: reportDocumentFilterData.value.mainDocument?.id,
        aggregation: reportDocumentFilterData.value.aggregation ?? null
      }),
      options: computed(() => ({
        enabled: !!indicesGroupsToExpand.value
      }))
    })

    const loading = computed<boolean>(() => indicesGroupsToExpandLoading.value || activeSheetLoading.value)

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      GridMode,
      bc,
      reportDocumentFilterData,
      reportRowGroupsFilter,
      reportRowGroups,
      reportRowGroupsItems,
      reportRowGroupsSearchFunction,
      activeSheetIndex,
      activeSheet,
      loading
    }
  }
})
</script>

<style lang="sass">
.report-sheets__left-navigator-container
  position: relative
  z-index: 0

  .v-card__title
    padding-bottom: 8px
</style>
