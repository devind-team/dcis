<template lang="pug">
  left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
    template(#header) {{ period.name }}
      template(v-if="hasPerm('dcis.add_document')")
        v-spacer
        add-document(:period-id="$route.params.periodId" :update="addDocumentUpdate")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Создать новый документ
    v-data-table(:headers="headers" :items="period.documents" disable-pagination hide-default-footer)
      template(#item.version="{ item }")
        nuxt-link(
          :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
        ) Версия {{ item.version }}
      template(#item.comment="{ item }")
        template(v-if="item.comment")
          text-menu(
            :value="item.comment"
            @update="changeDocumentComment(item, $event)"
            multiline
          )
            template(v-slot:default="{ on: onMenu }")
              v-tooltip(bottom)
                template(#activator="{ on: onTooltip }")
                  a(v-on="{...onMenu, ...onTooltip }") {{ item.comment }}
                span {{ $t('change') }}
      template(#item.lastStatus="{ item }")
        template(v-if="item.lastStatus")
          document-statuses(v-if="hasPerm('dcis.add_documentstatus')" :update="periodUpdate" :document="item")
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
import { defineComponent, inject, toRef, useNuxt2Meta } from '#app'
import { useAuthStore } from '~/store'
import { useFilters } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ChangeDocumentCommentMutation,
  ChangeDocumentCommentMutationPayload,
  ChangeDocumentCommentMutationVariables,
  DocumentType,
  PeriodType
} from '~/types/graphql'
import changeDocumentCommentMutation from '~/gql/dcis/mutations/document/change_document_comment.graphql'
import DocumentStatuses from '~/components/dcis/documents/DocumentStatuses.vue'
import AddDocument, { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import TextMenu from '~/components/common/menu/TextMenu.vue'

type ChangeDocumentCommentMutationResult = { data: { changeDocumentComment: ChangeDocumentCommentMutationPayload } }

export default defineComponent({
  components: { LeftNavigatorContainer, AddDocument, DocumentStatuses, TextMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: props.period.name })

    const userStore = useAuthStore()
    const hasPerm = toRef(userStore, 'hasPerm')

    const periodUpdate: any = inject('periodUpdate')
    const addDocumentUpdate = (cache: DataProxy, result: AddDocumentMutationResultType) => {
      periodUpdate(cache, result, (dataCache, { data: { addDocument: { success, document } } }: AddDocumentMutationResultType) => {
        if (success) {
          dataCache.period.documents = [document, ...dataCache.period.documents]
        }
        return dataCache
      })
    }

    const { mutate: ChangeDocumentCommentMutate } = useMutation<ChangeDocumentCommentMutation, ChangeDocumentCommentMutationVariables>(
      changeDocumentCommentMutation,
      {
        update: (cache, result) => periodUpdate(
          cache, result, (dataCache, { data: { changeDocumentComment: { document: doc } } }:
            ChangeDocumentCommentMutationResult) => {
            if (doc) {
              dataCache.period.documents = Object.assign(dataCache.period.documents, doc)
            }
            return dataCache
          })
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
      headers,
      hasPerm,
      periodUpdate,
      addDocumentUpdate,
      dateTimeHM,
      changeDocumentComment
    }
  }
})
</script>
