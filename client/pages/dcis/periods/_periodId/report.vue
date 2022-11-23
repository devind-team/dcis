<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.report.name') }}
    v-spacer
    report-settings-menu(v-slot="{ on, attrs }")
      v-btn(v-on="on" v-bind="attrs" icon)
        v-icon mdi-cog
  query-data-filter(
    v-model="selectedDocuments"
    :title="$tc(`dcis.periods.report.filters.documentsFilter.title`)"
    :message-function="documentFilterMessageFunction"
    :query="documentsQuery"
    :variables="{ periodId: period.id, divisionIds: [], lastStatusIds: [] }"
    :update="data => data.documents.edges.map(e => e.node)"
    :get-name="document => document.objectName"
    multiple
    modal
    fullscreen
  )
    template(#items="{ searchItems, tempItems, setSelected, setAllSelected }")
      v-data-table(
        :value="tempItems"
        :headers="documentsFilterTableHeaders"
        :items="searchItems"
        show-select
        disable-sort
        disable-pagination
        hide-default-footer
        @item-selected="setSelected($event.item, $event.value)"
        @toggle-select-all="setAllSelected($event.value)"
      )
        template(#item.division="{ item }") {{ item.objectName }} ({{ item.objectId }})
        template(#item.lastStatus="{ item }")
          div {{ item.lastStatus.status.name }}.
          div {{ $t('dcis.documents.tableItems.statusAssigned', { assigned: dateTimeHM(item.lastStatus.createdAt) }) }}
          .font-italic {{ item.lastStatus.comment }}
        template(
          v-for="dti in ['createdAt', 'updatedAt']"
          v-slot:[`item.${dti}`]="{ item }"
        ) {{ dateTimeHM(item[dti]) }}
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.READ"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
  )
</template>

<script lang="ts">
import { computed, defineComponent, ref, PropType, inject } from '#app'
import { DataTableHeader } from 'vuetify'
import { useCommonQuery, useFilters, useI18n } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, DocumentType, DocumentsSheetQuery, DocumentsSheetQueryVariables } from '~/types/graphql'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'
import documentsSheetQuery from '~/gql/dcis/queries/documents_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ReportSettingsMenu from '~/components/dcis/periods/ReportSettingsMenu.vue'
import QueryDataFilter from '~/components/common/filters/QueryDataFilter.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    ReportSettingsMenu,
    QueryDataFilter,
    GridSheets
  },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { dateTimeHM } = useFilters()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.report.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-report' }),
        exact: true
      }
    ]))

    const selectedDocuments = ref<DocumentType[]>([])
    const documentFilterMessageFunction = (selectedItems: DocumentType[]): string => {
      if (selectedItems.length === 0) {
        return t('dcis.periods.report.filters.documentsFilter.noFiltrationMessage') as string
      }
      return t('dcis.periods.report.filters.documentsFilter.multipleMessage', { count: selectedItems.length }) as string
    }
    const documentsFilterTableHeaders = computed<DataTableHeader[]>(() => [
      {
        text: t(`dcis.documents.tableHeaders.${props.period.project.contentType.model}`) as string,
        value: 'division'
      },
      { text: t('dcis.documents.tableHeaders.version') as string, value: 'version' },
      { text: t('dcis.documents.tableHeaders.comment') as string, value: 'comment' },
      { text: t('dcis.documents.tableHeaders.lastStatus') as string, value: 'lastStatus' },
      { text: t('dcis.documents.tableHeaders.createdAt') as string, value: 'createdAt' },
      { text: t('dcis.documents.tableHeaders.updatedAt') as string, value: 'updatedAt' }
    ])

    const activeSheetIndex = ref<number>(0)
    const { data: activeSheet } = useCommonQuery<
      DocumentsSheetQuery,
      DocumentsSheetQueryVariables
    >({
      document: documentsSheetQuery,
      variables: () => ({
        sheetId: props.period.sheets[activeSheetIndex.value].id,
        documentIds: selectedDocuments.value.map((document: DocumentType) => document.id)
      })
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      GridMode,
      documentsQuery,
      dateTimeHM,
      bc,
      selectedDocuments,
      documentFilterMessageFunction,
      documentsFilterTableHeaders,
      activeSheetIndex,
      activeSheet
    }
  }
})
</script>
