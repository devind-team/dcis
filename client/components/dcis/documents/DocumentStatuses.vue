<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.documents.status.header'))"
    :subheader="`Версия ${ document.version }`"
    :button-text="String($t('dcis.documents.status.buttonText'))"
    :mutation="require('~/gql/dcis/mutations/document/add_document_status.graphql')"
    :variables="{ documentId: document.id, statusId: status && status.id, comment }"
    :update="addDocumentStatusUpdate"
    mutation-name="addDocumentStatus"
    i18n-path="dcis.documents.status"
    persistent
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-list(two-line dense)
        v-list-item(v-for="item in documentStatuses" :key="item.id")
          v-list-item-content
            v-list-item-title {{ item.status.name }}
            v-list-item-subtitle {{ dateTimeHM(item.createdAt) }}
            v-list-item-subtitle {{ getUserName(item.user) }}
          v-list-item-content
            v-list-item-subtitle.font-italic {{ item.comment }}
          v-list-item-action(v-if="documentStatuses.length > 1 && hasPerm('dcis.delete_documentstatus')" )
            v-btn(@click="deleteDocumentStatus({ documentStatusId: item.id }).then()" icon)
              v-icon(color="error") mdi-close-circle
      v-divider
      v-text-field(v-model="comment" :label="$t('dcis.documents.status.comment')" success)
      v-combobox(
        v-model="status"
        :items="statuses"
        :label="$t('dcis.documents.status.name')"
        item-text="name"
        item-value="id"
        success
      )
</template>

<script lang="ts">
import { ApolloCache, DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import type { PropType, Ref } from '#app'
import { defineComponent, ref, toRef } from '#app'
import {
  AddDocumentStatusMutationPayload,
  DeleteDocumentStatusMutation,
  DeleteDocumentStatusMutationPayload,
  DeleteDocumentStatusMutationVariables,
  DocumentStatusesQuery,
  DocumentStatusesQueryVariables,
  DocumentType,
  StatusesQuery,
  StatusesQueryVariables,
  StatusType
} from '~/types/graphql'
import { useCommonQuery, useFilters } from '~/composables'
import { HasPermissionFnType, useAuthStore } from '~/store'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import documentStatusesQuery from '~/gql/dcis/queries/document_statuses.graphql'
import deleteDocumentStatusMutation from '~/gql/dcis/mutations/document/delete_document_status.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentStatusMutationResult = { data: { addDocumentStatus: AddDocumentStatusMutationPayload } }
export type DeleteDocumentStatusMutationResult = { data: { deleteDocumentStatus: DeleteDocumentStatusMutationPayload } }

type PeriodUpdateType = (
  cache: DataProxy | ApolloCache<any>,
  result: AddDocumentStatusMutationResult | DeleteDocumentStatusMutationResult,
  transform: (cache: any, result: AddDocumentStatusMutationResult | DeleteDocumentStatusMutationResult) => any
) => void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    update: { type: Function as PropType<PeriodUpdateType>, required: true }
  },
  setup (props) {
    const userStore = useAuthStore()
    const { dateTimeHM, getUserName } = useFilters()
    const hasPerm: Ref<HasPermissionFnType> = toRef(userStore, 'hasPerm')
    const comment: Ref<string> = ref<string>('')
    const status: Ref<StatusType | null> = ref<StatusType | null>(null)

    const { data: statuses, onResult } = useCommonQuery<StatusesQuery, StatusesQueryVariables>({
      document: statusesQuery
    })
    onResult(({ data: { statuses } }) => {
      status.value = statuses[0]
    })

    const {
      data: documentStatuses,
      addUpdate,
      deleteUpdate
    } = useCommonQuery<DocumentStatusesQuery, DocumentStatusesQueryVariables>({
      document: documentStatusesQuery,
      variables: { documentId: props.document.id }
    })

    const addDocumentStatusUpdate = (cache: DataProxy, result: AddDocumentStatusMutationResult) => {
      const { success } = result.data.addDocumentStatus
      if (success) {
        addUpdate(cache, result, 'documentStatus')
        props.update(cache, result, (dataCache, { data: { addDocumentStatus: { documentStatus } } }: AddDocumentStatusMutationResult) => {
          dataCache.period.documents.find(d => d.id === props.document.id).lastStatus = documentStatus
          return dataCache
        })
      }
    }

    const { mutate: deleteDocumentStatus } = useMutation<DeleteDocumentStatusMutation, DeleteDocumentStatusMutationVariables>(
      deleteDocumentStatusMutation,
      {
        update: (cache, result) => {
          deleteUpdate(cache, result)
          props.update(
            cache as any,
            result as DeleteDocumentStatusMutationResult,
            (dataCache, { data: { deleteDocumentStatus: { success, id } } }: DeleteDocumentStatusMutationResult) => {
              if (success) {
                dataCache.period
                  .documents.find(d => d.id === props.document.id)
                  .lastStatus = documentStatuses.value.filter(d => d.id !== id)[0]
              }
              return dataCache
            }
          )
        }
      })

    const close = () => {
      status.value = statuses[0]
      comment.value = ''
    }
    return {
      comment,
      status,
      statuses,
      documentStatuses,
      hasPerm,
      dateTimeHM,
      getUserName,
      addDocumentStatusUpdate,
      deleteDocumentStatus,
      close
    }
  }
})
</script>
