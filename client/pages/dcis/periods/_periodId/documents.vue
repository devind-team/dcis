<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-card
      v-card-title {{ period.name }}
        template(v-if="hasPerm('dcis.add_document')")
          v-spacer
          v-dialog(v-model="active" width="600")
            template(#activator="{ on }")
              v-btn(v-on="on" color="primary") Создать новый документ
            validation-observer(v-slot="{ handleSubmit, invalid }")
              form(@submit.prevent="handleSubmit(addDocument)")
                v-card
                  v-card-title Создать новый документ
                  v-card-text
                    validation-provider(name="Комментарий" rules="required" v-slot="{ errors, valid }")
                      v-text-field(v-model="comment" :error-messages="errors" :success="valid" label="Комментарий")
                    validation-provider(name="Статус" rules="required" v-slot="{ errors, valid }")
                      v-combobox(v-model="status" :items="statuses" label="Статус" item-text="name" item-value="id")
                  v-card-actions
                    v-btn(@click="active = false") Закрыть
                    v-spacer
                    v-btn(
                      :loading="loading"
                      :disabled="invalid"
                      type="submit"
                      color="primary"
                    ) Создать
      v-card-subtitle {{ period.project.name }}
      v-card-text
        v-data-table(:headers="headers" :items="period.documents" disable-pagination hide-default-footer)
          template(#item.version="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-documents-documentId', params: { documentId: item.id } })"
            ) Версия {{ item.version }}
          template(#item.lastStatus="{ item }")
            template(v-if="item.lastStatus")
              status(
                :document="item"
                :statuses="statuses"
                :doc-statuses="documentStatuses"
                :delete-status="deleteStatusUpdate"
                :update="addDocumentStatusUpdate"
                :user="user"
              )
                template(#activator="{ on }")
                  a(v-on="on" class="font-weight-bold") {{ item.lastStatus.status.name }}.
              div Назначен: {{ dateTimeHM(item.lastStatus.createdAt) }}
              .font-italic {{ item.lastStatus.comment }}
            template(v-else) Не установлен.
          template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import type { PropType, Ref } from '#app'
import { defineComponent, ref, useNuxt2Meta, inject, useRoute, toRefs } from '#app'
import { DataProxy } from 'apollo-cache'
import { useCommonQuery, useFilters } from '~/composables'
import { useAuthStore } from '~/store'
import { BreadCrumbsItem } from '~/types/devind'
import {
  AddDocumentMutation,
  AddDocumentMutationPayload,
  AddDocumentMutationVariables,
  PeriodType,
  StatusesQuery,
  StatusesQueryVariables,
  StatusType,
  DocumentStatusesQuery,
  DocumentStatusesQueryVariables,
  DeletedDocumentStatusMutation,
  DeletedDocumentStatusMutationVariables,
  DocumentStatusType
} from '~/types/graphql'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import addDocumentMutation from '~/gql/dcis/mutations/document/add_document.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import Status, { AddDocumentStatusMutationResult } from '~/components/dcis/projects/Status.vue'
import documentStatusesQuery from '~/gql/dcis/queries/document_statuses.graphql'
import deleteStatus from '~/gql/dcis/mutations/document/delete_status.graphql'

type AddDocumentMutationResultType = { data: { addDocument: AddDocumentMutationPayload } }

export default defineComponent({
  components: { BreadCrumbs, Status },
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
    const { hasPerm, user } = toRefs(userStore)
    const active: Ref<boolean> = ref<boolean>(false)
    const comment: Ref<string> = ref<string>('')
    const status: Ref<StatusType | null> = ref<StatusType | null>(null)

    const { data: statuses, onResult } = useCommonQuery<StatusesQuery, StatusesQueryVariables>({
      document: statusesQuery
    })
    onResult(({ data: { statuses } }) => {
      status.value = statuses[0]
    })

    const periodUpdate: any = inject('periodUpdate')
    const { mutate, loading } = useMutation<AddDocumentMutation, AddDocumentMutationVariables>(addDocumentMutation, {
      update: (cache, result) => periodUpdate(cache, result, (dataCache, { data: { addDocument: { success, document } } }: AddDocumentMutationResultType) => {
        if (success) {
          active.value = false
          dataCache.period.documents = [document, ...dataCache.period.documents]
        }
        return dataCache
      })
    })

    const addDocument = () => {
      mutate({ comment: comment.value, periodId: route.params.periodId, statusId: Number(status.value.id) })
    }

    const addDocumentStatusUpdate = (cache: DataProxy, result: AddDocumentStatusMutationResult) => {
      periodUpdate(cache, result, (dataCache, { data: { addDocumentStatus: { success, document } } }) => {
        if (success) {
          const dataKey = Object.keys(dataCache)[0]
          dataCache[dataKey] = Object.assign(dataCache[dataKey], document)
        }
        return dataCache
      })
    }

    const {
      data: documentStatuses,
      update
    } = useCommonQuery<DocumentStatusesQuery, DocumentStatusesQueryVariables>({
      document: documentStatusesQuery
    })

    const { mutate: DeleteDocumentStatusMutate } = useMutation<DeletedDocumentStatusMutation,
      DeletedDocumentStatusMutationVariables>(deleteStatus, {
        update: (cache, result) => update(cache, result, (dataCache, { data: { deleteDocumentStatus: { success, deletedId } } }: any) => {
          if (success) {
            const dataKey = Object.keys(dataCache)[0]
            dataCache[dataKey] = dataCache[dataKey].filter((e: any) => e.id !== deletedId)
          }
          return dataCache
        })
      })

    const deleteStatusUpdate = (docStatus: DocumentStatusType): void => {
      DeleteDocumentStatusMutate({ id: docStatus.id })
    }

    const headers: DataTableHeader[] = [
      { text: 'Версия', value: 'version' },
      { text: 'Комментарий', value: 'comment' },
      { text: 'Дата создания', value: 'createdAt' },
      { text: 'Статус', value: 'lastStatus' }
    ]

    return {
      active,
      comment,
      status,
      headers,
      statuses,
      addDocument,
      loading,
      dateTimeHM,
      hasPerm,
      user,
      documentStatuses,
      addDocumentStatusUpdate,
      deleteStatusUpdate
    }
  }
})
</script>
