<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.report.name') }}
    v-spacer
    report-settings-menu(v-slot="{ on, attrs }")
      v-btn(v-on="on" v-bind="attrs" icon)
        v-icon mdi-cog
  report-document-filter(v-model="reportDocumentFilterData" :period="period")
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.READ"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
  )
</template>

<script lang="ts">
import { computed, defineComponent, ref, PropType, inject } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, ReportSheetQuery, ReportSheetQueryVariables } from '~/types/graphql'
import reportSheetQuery from '~/gql/dcis/queries/report_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ReportSettingsMenu from '~/components/dcis/periods/ReportSettingsMenu.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import ReportDocumentFilter, {
  ReportDocumentType,
  ReportDocumentFilterData
} from '~/components/dcis/periods/ReportDocumentFilter.vue'

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    ReportSettingsMenu,
    GridSheets,
    ReportDocumentFilter
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

    const reportDocumentFilterData = ref<ReportDocumentFilterData>({
      reportDocuments: [],
      mainDocument: null
    })

    const activeSheetIndex = ref<number>(0)
    const { data: activeSheet } = useCommonQuery<
      ReportSheetQuery,
      ReportSheetQueryVariables
    >({
      document: reportSheetQuery,
      variables: () => ({
        sheetId: props.period.sheets[activeSheetIndex.value].id,
        reportDocuments: reportDocumentFilterData.value.reportDocuments.map((rd: ReportDocumentType) => ({
          ...rd,
          documentId: rd.document.id
        })),
        mainDocumentId: reportDocumentFilterData.value.mainDocument?.id
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
      activeSheetIndex,
      activeSheet
    }
  }
})
</script>
