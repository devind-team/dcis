<template lang="pug">
mutation-modal-form(
  :header="header"
  :subheader="String($t('dcis.documents.status.subheader', { version: document.version }))"
  :button-text="String($t('dcis.documents.status.buttonText'))"
  :hide-actions="!canAdd"
  :mutation="require('~/gql/dcis/mutations/document/add_document_status.graphql')"
  :variables="{ documentId: document.id, statusId: status && status.id, comment }"
  :update="addDocumentStatusUpdate"
  mutation-name="addDocumentStatus"
  i18n-path="dcis.documents.status"
  @close="close"
  @done="refetchStatuses"
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
        v-list-item-action(v-if="canDelete && documentStatuses.length > 1")
          delete-menu(
            :item-name="String($t('dcis.documents.status.delete.itemName'))"
            @confirm="deleteDocumentStatus({ documentStatusId: item.id })"
          )
            template(#default="{ on: onMenu }")
              v-tooltip(bottom)
                template(#activator="{ on: onTooltip }")
                  v-list-item-action(v-on="{ ...onMenu, ...onTooltip }")
                    v-btn(color="error" icon)
                      v-icon mdi-delete
                span {{ $t('dcis.documents.status.delete.tooltip') }}
    template(v-if="canAdd")
      v-divider
      v-text-field(v-model="comment" :label="$t('dcis.documents.status.comment')" success)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String($t('dcis.documents.status.status'))"
        rules="required"
      )
        v-select(
          v-model="status"
          :error-messages="errors"
          :success="valid"
          :items="statuses"
          :label="$t('dcis.documents.status.status')"
          item-text="name"
          item-value="id"
          return-object
        )
      v-alert(v-if="status && status.comment" type="warning" dense) {{ status.comment }}
</template>

<script lang="ts">
import { ApolloCache, DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import type { PropType } from '#app'
import { computed, defineComponent, ref } from '#app'
import {
  AddDocumentStatusMutationPayload,
  DeleteDocumentStatusMutation,
  DeleteDocumentStatusMutationPayload,
  DeleteDocumentStatusMutationVariables,
  DocumentStatusesQuery,
  DocumentStatusesQueryVariables,
  DocumentType,
  NewStatusesQuery,
  NewStatusesQueryVariables,
  StatusType
} from '~/types/graphql'
import { useCommonQuery, useFilters } from '~/composables'
import newStatusesQuery from '~/gql/dcis/queries/new_statuses.graphql'
import documentStatusesQuery from '~/gql/dcis/queries/document_statuses.graphql'
import deleteDocumentStatusMutation from '~/gql/dcis/mutations/document/delete_document_status.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export type AddDocumentStatusMutationResult = { data: { addDocumentStatus: AddDocumentStatusMutationPayload } }
export type DeleteDocumentStatusMutationResult = { data: { deleteDocumentStatus: DeleteDocumentStatusMutationPayload } }

type PeriodUpdateType = (
  cache: DataProxy | ApolloCache<any>,
  result: AddDocumentStatusMutationResult | DeleteDocumentStatusMutationResult,
  transform: (cache: any, result: AddDocumentStatusMutationResult | DeleteDocumentStatusMutationResult) => any
) => void

export default defineComponent({
  components: { MutationModalForm, DeleteMenu },
  props: {
    canAdd: { type: Boolean, required: true },
    canDelete: { type: Boolean, required: true },
    document: { type: Object as PropType<DocumentType>, required: true },
    update: { type: Function as PropType<PeriodUpdateType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()
    const { dateTimeHM, getUserName } = useFilters()

    const header = computed<string>(() => props.canAdd || props.canDelete
      ? t('dcis.documents.status.header') as string
      : t('dcis.documents.status.readonlyHeader') as string
    )

    const comment = ref<string>('')
    const status = ref<StatusType | null>(null)

    const { data: statuses, onResult, refetch: refetchStatuses } = useCommonQuery<
      NewStatusesQuery,
      NewStatusesQueryVariables
    >({
      document: newStatusesQuery,
      variables: () => ({
        documentId: props.document.id
      })
    })

    onResult(({ data: { newStatuses } }) => {
      nextTick(() => { status.value = newStatuses[0] || null })
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
        props.update(
          cache,
          result,
          (
            dataCache,
            { data: { addDocumentStatus: { documentStatus } } }: AddDocumentStatusMutationResult
          ) => {
            dataCache.documents.edges.find(d => d.node.id === props.document.id).node.lastStatus = documentStatus
            return dataCache
          })
      }
    }

    const { mutate: deleteDocumentStatusMutate } = useMutation<
      DeleteDocumentStatusMutation,
      DeleteDocumentStatusMutationVariables
    >(
      deleteDocumentStatusMutation,
      {
        update: (cache, result) => {
          deleteUpdate(cache, result)
          props.update(
            cache as any,
            result as DeleteDocumentStatusMutationResult,
            (
              dataCache,
              { data: { deleteDocumentStatus: { errors, id } } }: DeleteDocumentStatusMutationResult
            ) => {
              if (!errors.length) {
                dataCache.documents.edges.find(d => d.node.id === props.document.id).node.lastStatus =
                  documentStatuses.value.filter(d => d.id !== id)[0]
              }
              return dataCache
            }
          )
        }
      })
    const deleteDocumentStatus = async (variables: DeleteDocumentStatusMutationVariables) => {
      await deleteDocumentStatusMutate(variables)
      await refetchStatuses()
    }

    const close = () => {
      status.value = statuses.value[0] || null
      comment.value = ''
    }

    return {
      header,
      comment,
      status,
      statuses,
      refetchStatuses,
      documentStatuses,
      dateTimeHM,
      getUserName,
      addDocumentStatusUpdate,
      deleteDocumentStatus,
      close
    }
  }
})
</script>
