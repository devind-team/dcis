<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.documents.status.header'))"
    :subheader="`Версия ${ document.version }`"
    :button-text="String($t('dcis.documents.status.buttonText'))"
    :mutation="addDocumentStatus"
    :variables="{ documentId: document.id, userId: user.id, statusId: status.id, comment }"
    :update="addDocumentStatusUpdate"
    mutation-name="addDocumentStatus"
    i18n-path="dcis.documents.status"
    persistent
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-combobox(
        v-model="status"
        :items="statuses"
        :label="$t('dcis.documents.status.name')"
        item-text="name"
        item-value="id"
        success
      )
      v-text-field(
        v-model="comment"
        :label="$t('dcis.documents.status.comment')"
        success
      )
      v-list(two-line dense)
        v-divider
        template(v-for="item in documentStatuses")
          v-list-item(:key="item.id")
            v-list-item-content
              v-list-item-title {{ item.status.name }}
              v-list-item-subtitle {{ dateTimeHM(item.createdAt) }}
              v-list-item-subtitle {{ getUserName(item.user) }}
            v-list-item-content
              v-list-item-subtitle.font-italic {{ item.comment }}
            v-list-item-action(v-if="hasPerm('dcis.delete_documentstatus')" )
              v-btn(
                v-if="documentStatuses.length > 1"
                @click="deleteDocumentStatusMutate({ documentStatusId: item.id }).then()"
                icon
              )
                v-icon(color="error") mdi-close-circle
          v-divider
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import type { PropType, Ref } from '#app'
import { defineComponent, inject, ref, toRefs } from '#app'
import {
  AddDocumentStatusMutationPayload,
  DeleteDocumentStatusMutation,
  DeleteDocumentStatusMutationVariables,
  DocumentStatusesQuery,
  DocumentStatusesQueryVariables,
  DocumentType, StatusesQuery, StatusesQueryVariables,
  StatusType,
  UserType
} from '~/types/graphql'
import { useCommonQuery, useConvertors, useFilters } from '~/composables'
import { useAuthStore } from '~/store'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import documentStatusesQuery from '~/gql/dcis/queries/document_statuses.graphql'
import addDocumentStatusMutation from '~/gql/dcis/mutations/document/add_status.graphql'
import deleteStatus from '~/gql/dcis/mutations/document/delete_document_status.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentStatusMutationResult = { data: { addDocumentStatus: AddDocumentStatusMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    documentItem: { type: Object as PropType<DocumentType>, required: true },
    user: { type: Object as PropType<UserType>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()
    const { getUserName } = useConvertors()
    const userStore = useAuthStore()
    const { hasPerm } = toRefs(userStore)
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
      deleteUpdate,
      addUpdate
    } = useCommonQuery<DocumentStatusesQuery, DocumentStatusesQueryVariables>({
      document: documentStatusesQuery,
      variables: { documentId: props.document.id }
    })

    const periodUpdate: any = inject('periodUpdate')

    const addDocumentStatusUpdate = (cache: DataProxy, result: AddDocumentStatusMutationResult) => {
      addUpdate(cache, result, 'documentStatus')
      periodUpdate(cache, result, (dataCache, { data: { addDocumentStatus: { success, document } } }) => {
        if (success) {
          const dataKey = Object.keys(dataCache)[0]
          dataCache[dataKey] = Object.assign(dataCache[dataKey], document)
        }
        return dataCache
      })
    }

    const { mutate: deleteDocumentStatusMutate } = useMutation<DeleteDocumentStatusMutation, DeleteDocumentStatusMutationVariables>(
      deleteStatus,
      {
        update: (cache, result) => {
          deleteUpdate(cache, result)
          periodUpdate(cache, result, (dataCache, { data: { deleteDocumentStatus: { success, document } } }: any) => {
            if (success) {
              const dataKey = Object.keys(dataCache)[0]
              dataCache[dataKey] = Object.assign(dataCache[dataKey], document)
            }
            return dataCache
          })
        }
      })

    const close = () => {
      status.value = null
      comment.value = ''
    }
    return {
      comment,
      status,
      statuses,
      addDocumentStatusUpdate,
      addDocumentStatusMutation,
      dateTimeHM,
      close,
      hasPerm,
      getUserName,
      documentStatuses,
      deleteDocumentStatusMutate
    }
  }
})
</script>
