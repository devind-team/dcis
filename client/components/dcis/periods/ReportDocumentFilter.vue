<template lang="pug">
items-data-filter(
  v-model="reportDocuments"
  :items="reportDocumentItems"
  :title="String($t(`dcis.periods.report.documentsFilter.title`))"
  :get-key="reportDocument => reportDocument.document.id"
  :get-name="reportDocument => reportDocument.document.objectName"
  :message-container-class="messageContainerClass"
  multiple
  modal
  fullscreen
  @active-changed="activeChanged"
  @temp-items-changed="tempItemsChanged"
  @clear="clear"
  @close="close"
  @reset="reset"
  @apply="apply"
)
  template(#message="message")
    slot(name="message" v-bind="message")
  template(#fixed-content="{ tempItems }")
    v-card-text(style="flex: none")
      v-chip.mr-1(
        :class="{'font-weight-bold': !!mainDocument}"
        :close="!!mainDocument || mainDocumentSelection"
        :disabled="!tempItems.length"
        @click="startMainDocumentSelection"
        @click:close="closeMainDocument"
      ) {{ mainDocumentMessage }}
      items-data-filter(
        v-model="aggregation"
        :items="aggregationItems"
        :title="String($t('dcis.periods.report.documentsFilter.aggregationFilter.title'))"
        :disabled="!tempItems.length"
        :message-function="aggregationMessageFunction"
        :get-name="item => String($t(`dcis.periods.report.documentsFilter.aggregationFilter.${item.id.toLowerCase()}`))"
      )
  template(#items="{ searchItems, tempItems, setSelected, setAllSelected }")
    v-data-table(
      :value="tempItems"
      :headers="documentsFilterTableHeaders"
      :items="getItems(searchItems, tempItems)"
      :show-select="!mainDocumentSelection"
      item-key="document.id"
      disable-sort
      disable-pagination
      hide-default-footer
      @item-selected="setSelected($event.item, $event.value)"
      @toggle-select-all="setAllSelected($event.value)"
    )
      template(#item="{ item, isSelected, select }")
        tr(
          :class="{ 'font-weight-bold': !!mainDocument && item.document.id === mainDocument.id }"
          :style="{ 'background-color': item.color ? item.color : 'transparent' }"
        )
          td.text-center(v-if="mainDocumentSelection")
            v-tooltip(bottom)
              template(#activator="{ on, attrs }")
                v-btn(v-on="on" v-bind="attrs" color="success" icon @click="selectMainDocument(item.document)")
                  v-icon mdi-check-circle
              span {{ $t('dcis.periods.report.documentsFilter.selectMainDocument') }}
          td.text-center(v-else)
            v-simple-checkbox(v-ripple :value="isSelected" @input="select($event)")
          td {{ item.document.objectName }} ({{ item.document.objectId }})
          td {{ item.document.version }}
          td
            div {{ item.document.lastStatus.status.name }}.
            div {{ $t('dcis.documents.tableItems.statusAssigned', { assigned: dateTimeHM(item.document.lastStatus.createdAt) }) }}
            .font-italic {{ item.document.lastStatus.comment }}
          td {{ dateTimeHM(item.document.createdAt) }}
          td {{ dateTimeHM(item.document.updatedAt) }}
          td.text-center(v-if="!mainDocumentSelection")
            report-document-properties-form(
              v-if="!!tempItems.find(i => i.document.id === item.document.id)"
              :document="item.document"
              :is-visible.sync="item.isVisible"
              :color.sync="item.color"
            )
              template(#activator="{ on: onDialog, attrs: attrsDialog }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip, attrs: attrsTooltip }")
                    v-btn(
                      v-on="{ ...onDialog, ...onTooltip }"
                      v-bind="{ ...attrsDialog, ...attrsTooltip }"
                      color="primary"
                      icon
                    )
                      v-icon mdi-pencil
                  span {{ $t('dcis.periods.report.documentsFilter.propertiesForm.buttonText') }}
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch, onMounted, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { useMutationObserver } from '@vueuse/core'
import { Class, GetName } from '~/types/filters'
import { PeriodType, DocumentType, DocumentsQuery, DocumentsQueryVariables, ReportAggregation } from '~/types/graphql'
import { useFilters, useI18n, useQueryRelay } from '~/composables'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import ReportDocumentPropertiesForm from '~/components/dcis/periods/ReportDocumentPropertiesForm.vue'

export type ReportDocumentType = {
  document: DocumentType,
  isVisible: boolean,
  color: string | null
}
export type ReportDocumentFilterInputType = {
  reportDocuments: ReportDocumentType[],
  mainDocument: DocumentType | null,
  aggregation: ReportAggregation | null
}
type AggregationItemType = { id: ReportAggregation }

export default defineComponent({
  components: { ItemsDataFilter, ReportDocumentPropertiesForm },
  props: {
    value: { type: Object as PropType<ReportDocumentFilterInputType>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()
    const { dateTimeHM } = useFilters()

    const reportDocuments = ref<ReportDocumentType[]>([])

    const mainDocument = ref<DocumentType | null>(null)
    const mainDocumentSelection = ref<boolean>(false)
    const mainDocumentMessage = computed<string>(() => {
      if (mainDocumentSelection.value) {
        return t('dcis.periods.report.documentsFilter.mainDocumentSelection') as string
      }
      if (mainDocument.value) {
        return t(
          'dcis.periods.report.documentsFilter.mainDocument',
          { divisionId: mainDocument.value.objectId }
        ) as string
      }
      return t('dcis.periods.report.documentsFilter.selectMainDocument') as string
    })
    const startMainDocumentSelection = () => {
      mainDocumentSelection.value = true
    }
    const selectMainDocument = (md: DocumentType) => {
      mainDocument.value = md
      mainDocumentSelection.value = false
    }
    const closeMainDocument = () => {
      if (mainDocumentSelection.value) {
        mainDocumentSelection.value = false
      } else if (mainDocument.value) {
        mainDocument.value = null
      }
    }

    const aggregation = ref<AggregationItemType | null>(null)
    const aggregationItems: AggregationItemType[] = [
      { id: 'CONCAT' },
      { id: 'SUM' },
      { id: 'AVG' },
      { id: 'MIN' },
      { id: 'MAX' }
    ]
    const aggregationMessageFunction = (selectedItems: AggregationItemType[], getName: GetName): string => {
      if (selectedItems.length) {
        return t(
          'dcis.periods.report.documentsFilter.aggregationFilter.aggregation',
          { method: getName(selectedItems[0]) }
        ) as string
      }
      return t('dcis.periods.report.documentsFilter.aggregationFilter.selectAggregation') as string
    }

    const { data: documents } = useQueryRelay<DocumentsQuery, DocumentsQueryVariables, DocumentType>({
      document: documentsQuery,
      variables: () => ({
        periodId: props.period.id,
        divisionIds: [],
        lastStatusIds: []
      })
    })
    const reportDocumentItems = ref<ReportDocumentType[]>([])
    watch(() => documents.value, (newValue: DocumentType[] | undefined) => {
      if (newValue) {
        if (newValue.length > reportDocumentItems.value.length) {
          const newDocuments = newValue.filter((d: DocumentType) =>
            !reportDocumentItems.value.find((r: ReportDocumentType) => r.document.id === d.id)
          )
          for (const newDocument of newDocuments) {
            reportDocumentItems.value.push({
              document: newDocument,
              isVisible: true,
              color: null
            })
          }
        } else {
          reportDocumentItems.value = reportDocumentItems.value.filter((r: ReportDocumentType) =>
            !!newValue.find((d: DocumentType) => d.id === r.document.id)
          )
        }
      }
    }, { immediate: true })
    const getItems = (searchItems: ReportDocumentType[], tempItems: ReportDocumentType[]): ReportDocumentType[] => {
      if (mainDocumentSelection.value) {
        return tempItems.filter(
          (tempItem: ReportDocumentType) => !!searchItems.find(
            (searchItem: ReportDocumentType) => searchItem.document.id === tempItem.document.id
          )
        )
      }
      return searchItems
    }

    const documentsFilterTableHeaders = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = []
      if (mainDocumentSelection.value) {
        result.push({ text: '', value: 'mainDocument', align: 'center', filterable: false, sortable: false })
      }
      result.push(...[
        {
          text: t(`dcis.documents.tableHeaders.${props.period.project.contentType.model}`) as string,
          value: 'division'
        },
        { text: t('dcis.documents.tableHeaders.version') as string, value: 'version' },
        { text: t('dcis.documents.tableHeaders.lastStatus') as string, value: 'lastStatus' },
        { text: t('dcis.documents.tableHeaders.createdAt') as string, value: 'createdAt' },
        { text: t('dcis.documents.tableHeaders.updatedAt') as string, value: 'updatedAt' }
      ])
      if (!mainDocumentSelection.value) {
        result.push({
          text: t('actions') as string,
          value: 'actions',
          align: 'center',
          filterable: false,
          sortable: false
        })
      }
      return result
    })

    const active = ref<boolean>(false)
    const activeChanged = (value: boolean) => {
      active.value = value
    }
    onMounted(() => {
      useMutationObserver(document.documentElement, (mutations) => {
        if (mutations[0] && active.value && !document.documentElement.classList.contains('overflow-y-hidden')) {
          document.documentElement.classList.add('overflow-y-hidden')
        }
      }, {
        attributeFilter: ['class']
      })
    })

    const tempItemsChanged = (reportDocuments: ReportDocumentType[]) => {
      if (!reportDocuments.length) {
        aggregation.value = null
      }
      if (!mainDocument.value) {
        return
      }
      if (!reportDocuments.find((rd: ReportDocumentType) => rd.document.id === mainDocument.value.id)) {
        mainDocument.value = null
      }
    }

    const clearReportDocumentItems = () => {
      for (const reportDocument of reportDocumentItems.value) {
        reportDocument.isVisible = true
        reportDocument.color = null
      }
    }

    const closeReportDocumentItems = () => {
      for (const reportDocument of reportDocumentItems.value) {
        const valueReportDocument = props.value.reportDocuments.find(
          (valueReportDocument: ReportDocumentType) => valueReportDocument.document.id === reportDocument.document.id
        )
        if (valueReportDocument) {
          reportDocument.isVisible = valueReportDocument.isVisible
          reportDocument.color = valueReportDocument.color
        } else {
          reportDocument.isVisible = true
          reportDocument.color = null
        }
      }
    }

    const clear = () => {
      mainDocument.value = null
      aggregation.value = null
      clearReportDocumentItems()
      emit('clear')
    }

    const close = () => {
      mainDocument.value = props.value.mainDocument
      mainDocumentSelection.value = false
      aggregation.value = props.value.aggregation ? { id: props.value.aggregation } : null
      closeReportDocumentItems()
      emit('close')
    }

    const reset = () => {
      mainDocument.value = null
      mainDocumentSelection.value = false
      aggregation.value = null
      clearReportDocumentItems()
      emit('reset')
    }

    const apply = () => {
      emit('input', {
        reportDocuments: reportDocuments.value.map((rd: ReportDocumentType) => ({ ...rd })),
        mainDocument: mainDocument.value,
        aggregation: aggregation.value ? aggregation.value.id : null
      })
      emit('apply')
    }

    return {
      dateTimeHM,
      reportDocuments,
      mainDocument,
      mainDocumentSelection,
      mainDocumentMessage,
      startMainDocumentSelection,
      selectMainDocument,
      closeMainDocument,
      aggregation,
      aggregationItems,
      aggregationMessageFunction,
      reportDocumentItems,
      getItems,
      documentsFilterTableHeaders,
      activeChanged,
      tempItemsChanged,
      clear,
      close,
      reset,
      apply
    }
  }
})
</script>
