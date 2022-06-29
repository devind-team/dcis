<template lang="pug">
  left-navigator-container(@update-drawer="$emit('update-drawer')" :bread-crumbs="breadCrumbs")
    template(#header) {{ period.name }}
      template(v-if="hasPerm('dcis.add_document')")
        v-spacer
        add-document(:period="period" :documents="documents" :update="addDocumentUpdate")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Создать новый документ
    v-row
      v-col(cols="12" sm="9")
      v-col.text-right(cols="12" sm="3") {{ $t('shownOf', { totalCount, count }) }}
    v-data-table(:headers="headers" :items="documents" :loading="loading" disable-pagination hide-default-footer)
      template(#item.version="{ item }")
        nuxt-link(
          :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
        ) Версия {{ item.version }}
      template(#item.comment="{ item }")
        template(v-if="item.comment")
          text-menu(v-slot="{ on }" @update="changeDocumentComment(item, $event)" :value="item.comment")
            a(v-on="on") {{ item.comment }}
      template(#item.lastStatus="{ item }")
        template(v-if="item.lastStatus")
          document-statuses(v-if="hasPerm('dcis.add_documentstatus')" :update="update" :document="item")
            template(#activator="{ on }")
              a(v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
          strong(v-else) {{ item.lastStatus.status.name }}.
          div Назначен: {{ dateTimeHM(item.lastStatus.createdAt) }}
          .font-italic {{ item.lastStatus.comment }}
      template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { defineComponent, toRef, useNuxt2Meta } from '#app'
import { useAuthStore } from '~/stores'
import { useFilters } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangeDocumentCommentMutation,
  ChangeDocumentCommentMutationVariables,
  DocumentsQuery,
  DocumentsQueryVariables,
  DocumentType,
  PeriodType
} from '~/types/graphql'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'
import changeDocumentCommentMutation from '~/gql/dcis/mutations/document/change_document_comment.graphql'
import DocumentStatuses from '~/components/dcis/documents/DocumentStatuses.vue'
import AddDocument, { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import TextMenu from '~/components/common/menu/TextMenu.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, AddDocument, DocumentStatuses, TextMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })

    const userStore = useAuthStore()
    const hasPerm = toRef(userStore, 'hasPerm')

    const {
      data: documents,
      loading,
      pagination: { count, totalCount },
      update,
      addUpdate,
      changeUpdate
    } = useQueryRelay<DocumentsQuery, DocumentsQueryVariables, DocumentType>({
      document: documentsQuery,
      variables: () => ({ periodId: route.params.periodId })
    })

    const addDocumentUpdate = (cache: DataProxy, result: AddDocumentMutationResultType) => {
      if (!result.data.addDocument.errors.length) {
        addUpdate(cache, result, 'document')
      }
    }

    const { mutate: ChangeDocumentCommentMutate } = useMutation<ChangeDocumentCommentMutation, ChangeDocumentCommentMutationVariables>(
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
    const headers: DataTableHeader[] = [
      { text: 'Версия', value: 'version' },
      { text: 'Комментарий', value: 'comment' },
      { text: 'Дата создания', value: 'createdAt' },
      { text: 'Статус', value: 'lastStatus' }
    ]

    return {
      documents,
      loading,
      headers,
      hasPerm,
      count,
      totalCount,
      update,
      addDocumentUpdate,
      dateTimeHM,
      changeDocumentComment
    }
  }
})
</script>
