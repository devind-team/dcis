<template lang="pug">
left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.documents.name') }}
    template(v-if="period.canAddDocument")
      v-spacer
      add-document(:period="period" :documents="documents" :update="addDocumentUpdate")
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ $t('dcis.documents.addDocument.buttonText') }}
  template(#subheader) {{ $t('shownOf', { count, totalCount }) }}
  items-data-filter(
    v-if="period.multiple"
    v-model="selectedDocs"
    :items="period.divisions.map( x => ({id: x.id, name: x.name}))"
    :get-name="i => i.name"
    multiple
  )
  v-data-table(:headers="headers" :items="visibleDocs" :loading="loading" disable-pagination hide-default-footer)
    template(#item.version="{ item }")
      nuxt-link(
        :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
      ) {{ $t('dcis.documents.tableItems.version', { version: item.version }) }}
    template(#item.comment="{ item }")
      template(v-if="item.comment")
        template(v-if="item.canChange")
          text-menu(v-slot="{ on }" @update="changeDocumentComment(item, $event)" :value="item.comment")
            a(v-on="on") {{ item.comment }}
        template(v-else) {{ item.comment }}
    template(#item.lastStatus="{ item }")
      template(v-if="item.lastStatus")
        document-statuses(v-if="item.canChange" :update="update" :document="item")
          template(#activator="{ on }")
            a(v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
        strong(v-else) {{ item.lastStatus.status.name }}.
        div {{ $t('dcis.documents.tableItems.statusAssigned', { assigned: dateTimeHM(item.lastStatus.createdAt) }) }}
        .font-italic {{ item.lastStatus.comment }}
    template(#item.division="{ item }") {{ item.objectId ? period.divisions.find(x => x.id === item.objectId).name : '-' }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { defineComponent, toRef, useNuxt2Meta } from '#app'
import { useAuthStore } from '~/stores'
import { useFilters, useI18n } from '~/composables'
import { useDocumentsQuery } from '~/services/grapqhl/queries/dcis/documents'
import { BreadCrumbsItem } from '~/types/devind'
import {
  DocumentType,
  PeriodType,
  ChangeDocumentCommentMutation,
  ChangeDocumentCommentMutationVariables
} from '~/types/graphql'
import changeDocumentCommentMutation from '~/gql/dcis/mutations/document/change_document_comment.graphql'
import DocumentStatuses from '~/components/dcis/documents/DocumentStatuses.vue'
import AddDocument, { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import TextMenu from '~/components/common/menu/TextMenu.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

type DivisionFilterType = { id: string, name: string }

export default defineComponent({
  components: { ItemsDataFilter, LeftNavigatorContainer, AddDocument, DocumentStatuses, TextMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const route = useRoute()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })
    const userStore = useAuthStore()
    const hasPerm = toRef(userStore, 'hasPerm')

    const {
      data: documents,
      loading,
      pagination: { totalCount },
      update,
      addUpdate,
      changeUpdate
    } = useDocumentsQuery(route.params.periodId)

    const addDocumentUpdate = (cache: DataProxy, result: AddDocumentMutationResultType) => {
      if (!result.data.addDocument.errors.length) {
        addUpdate(cache, result, 'document')
      }
    }

    const { mutate: ChangeDocumentCommentMutate } = useMutation<
      ChangeDocumentCommentMutation,
      ChangeDocumentCommentMutationVariables
    >(
      changeDocumentCommentMutation,
      {
        update: (cache, result) => {
          if (!result.errors) {
            changeUpdate(cache, result, 'document')
          }
        }
      }
    )

    const changeDocumentComment = (document: DocumentType, comment: string): void => {
      ChangeDocumentCommentMutate({ documentId: document.id, comment })
    }
    const headers: DataTableHeader[] = props.period.multiple
      ? [{
          text: t(`dcis.documents.tableHeaders.${props.period.project.contentType.model}`) as string,
          value: 'division'
        }]
      : []

    headers.push(
      { text: t('dcis.documents.tableHeaders.version') as string, value: 'version' },
      { text: t('dcis.documents.tableHeaders.comment') as string, value: 'comment' },
      { text: t('dcis.documents.tableHeaders.lastStatus') as string, value: 'lastStatus' }
    )
    const selectedDocs = ref<DivisionFilterType[]>([])
    const visibleDocs = computed<DocumentType[]>(() => {
      return selectedDocs.value.length > 0
        ? documents.value.filter(x => selectedDocs.value.map(x => x.id).includes(x.objectId))
        : documents.value
    })
    const count = computed(() => {
      return selectedDocs.value.length > 0 ? visibleDocs.value.length : totalCount.value
    })
    return {
      selectedDocs,
      documents,
      loading,
      headers,
      hasPerm,
      count,
      totalCount,
      update,
      visibleDocs,
      addDocumentUpdate,
      dateTimeHM,
      changeDocumentComment
    }
  }
})
</script>
