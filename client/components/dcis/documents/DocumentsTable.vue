<template lang="pug">
v-data-table(
  :headers="headers"
  :items="documents"
  :loading="loading"
  :custom-sort="customSort"
  disable-pagination
  hide-default-footer
  multi-sort
)
  template(#item.division="{ item }")
    nuxt-link(
      :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
    ) {{ item.objectName }} ({{ item.objectId }})
  template(#item.version="{ item }")
    template(v-if="period.multiple") {{ item.version }}
    nuxt-link(
      v-else
      :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
    ) {{ item.version }}
  template(#item.lastStatus="{ item }")
    template(v-if="item.lastStatus")
      document-statuses(
        :can-delete="canDeleteDocumentStatus(item)"
        :update="updateDocuments"
        :document="item"
        :period="period"
        @add-status="$emit('add-status')"
      )
        template(#activator="{ on }")
          a(v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
      div {{ $t('dcis.documents.tableItems.statusAssigned', { assigned: dateTimeHM(item.lastStatus.createdAt) }) }}
      .font-italic {{ item.lastStatus.comment }}
  template(v-for="dti in ['createdAt', 'updatedAt']" v-slot:[`item.${dti}`]="{ item }") {{ dateTimeHM(item[dti]) }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { useFilters, useI18n } from '~/composables'
import { collectOrderBy } from '~/services/ordering'
import { PeriodType, DocumentType } from '~/types/graphql'
import TextMenu from '~/components/common/menu/TextMenu.vue'
import DocumentStatuses, { PeriodUpdateType } from '~/components/dcis/documents/DocumentStatuses.vue'

export default defineComponent({
  components: { TextMenu, DocumentStatuses },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    documents: { type: Array as PropType<DocumentType[]>, required: true },
    loading: { type: Boolean, required: true },
    updateDocuments: { type: Function as PropType<PeriodUpdateType>, required: true }
  },
  setup (props, { emit }) {
    const { t } = useI18n()
    const { dateTimeHM } = useFilters()

    const headers = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = props.period.multiple
        ? [{
            text: t(`dcis.documents.tableHeaders.${props.period.project.contentType.model}`) as string,
            value: 'division'
          }]
        : []
      result.push(
        { text: t('dcis.documents.tableHeaders.version') as string, value: 'version' },
        { text: t('dcis.documents.tableHeaders.lastStatus') as string, value: 'lastStatus' },
        { text: t('dcis.documents.tableHeaders.createdAt') as string, value: 'createdAt' },
        { text: t('dcis.documents.tableHeaders.updatedAt') as string, value: 'updatedAt' }
      )
      return result
    })

    const canDeleteDocumentStatus = (document: DocumentType) => {
      return document.canChange
    }
    const customSort = (items: DocumentType[], sortBy: string[], sortDesc: boolean[]) => {
      emit('update-order-by', collectOrderBy(sortBy, sortDesc))
      return items
    }

    return { headers, canDeleteDocumentStatus, dateTimeHM, customSort }
  }
})
</script>
