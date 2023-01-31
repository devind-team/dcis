<template lang="pug">
mutation-modal-form(
  ref="form"
  :header="header"
  :subheader="String($t('dcis.documents.status.subheader', { version: document.version }))"
  :button-text="String($t('dcis.documents.status.buttonText'))"
  :hide-actions="!canAdd"
  :mutation="require('~/gql/dcis/mutations/document/add_document_status.graphql')"
  :variables="{ documentId: document.id, statusId: status && status.id, comment }"
  :update="addDocumentStatusUpdate"
  :hide-alert-timeout="Infinity"
  :table-errors-mode="ErrorValidateDialogMode.TABLE"
  :table-errors-message="String($t('dcis.documents.status.tableErrorsMessage'))"
  :table-errors-title="String($t('dcis.documents.status.tableErrorsTitle'))"
  :show-table-errors-search="false"
  mutation-name="addDocumentStatus"
  errors-in-alert
  @first-activated="firstActivated"
  @close="close"
  @done="addDocumentStatusDone"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    v-list(v-if="documentStatuses" two-line dense)
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
    v-progress-linear(v-else indeterminate)
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
          :loading="statusesLoading"
          :items="statuses"
          :label="$t('dcis.documents.status.status')"
          item-text="name"
          item-value="id"
          return-object
        )
      v-alert(v-if="status && status.comment" type="warning" dense) {{ status.comment }}
</template>

<script lang="ts">
import { WatchQueryFetchPolicy } from '@apollo/client'
import { ApolloCache, DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import type { PropType } from '#app'
import { computed, defineComponent, onMounted, ref, watch } from '#app'
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
  StatusType,
  StatusFieldsFragment
} from '~/types/graphql'
import { useCommonQuery, useFilters } from '~/composables'
import newStatusesQuery from '~/gql/dcis/queries/new_statuses.graphql'
import documentStatusesQuery from '~/gql/dcis/queries/document_statuses.graphql'
import deleteDocumentStatusMutation from '~/gql/dcis/mutations/document/delete_document_status.graphql'
import { ErrorValidateDialogMode } from '~/components/common/dialogs/ErrorValidateDialog.vue'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export type AddDocumentStatusMutationResult = { data: { addDocumentStatus: AddDocumentStatusMutationPayload } }
export type DeleteDocumentStatusMutationResult = { data: { deleteDocumentStatus: DeleteDocumentStatusMutationPayload } }

export type PeriodUpdateType = (
  cache: DataProxy | ApolloCache<any>,
  result: AddDocumentStatusMutationResult | DeleteDocumentStatusMutationResult,
  transform: (cache: any, result: AddDocumentStatusMutationResult | DeleteDocumentStatusMutationResult) => any
) => void

export default defineComponent({
  components: { MutationModalForm, DeleteMenu },
  props: {
    canDelete: { type: Boolean, required: true },
    document: { type: Object as PropType<DocumentType>, required: true },
    update: { type: Function as PropType<PeriodUpdateType>, required: true }
  },
  setup (props, { emit }) {
    const { t } = useI18n()
    const { dateTimeHM, getUserName } = useFilters()

    onMounted(() => {
      watch(() => statuses.value, (statuses: StatusFieldsFragment[]) => {
        if (statuses) {
          status.value = statuses[0] || null
        }
      }, { immediate: true })
    })

    const firstActivated = () => {
      statusesQueryOptions.value.enabled = true
      documentStatusesQueryOptions.value.enabled = true
    }

    const canAdd = computed<boolean>(() => Boolean(statuses.value && statuses.value.length))

    const header = computed<string>(() => canAdd.value || props.canDelete
      ? t('dcis.documents.status.header') as string
      : t('dcis.documents.status.readonlyHeader') as string
    )

    const comment = ref<string>('')
    const status = ref<StatusType | null>(null)

    const statusesQueryOptions = ref<{ enabled: boolean, fetchPolicy: WatchQueryFetchPolicy }>({
      enabled: false,
      fetchPolicy: 'cache-and-network'
    })
    const documentStatusesQueryOptions = ref<{ enabled: boolean }>({ enabled: false })
    const {
      data: statuses,
      loading: statusesLoading,
      refetch: refetchStatuses
    } = useCommonQuery<
      NewStatusesQuery,
      NewStatusesQueryVariables
    >({
      document: newStatusesQuery,
      variables: () => ({
        documentId: props.document.id
      }),
      options: statusesQueryOptions
    })
    const addDocumentStatusDone = () => {
      emit('add-status')
      refetchStatuses()
    }

    const {
      data: documentStatuses,
      addUpdate,
      deleteUpdate
    } = useCommonQuery<DocumentStatusesQuery, DocumentStatusesQueryVariables>({
      document: documentStatusesQuery,
      variables: { documentId: props.document.id },
      options: documentStatusesQueryOptions
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

    const deleteDocumentStatus = async () => {
      await deleteDocumentStatusMutate(deleteDocumentStatusVariables.value)
      await refetchStatuses()
    }

    const deleteDocumentStatusVariables = computed<DeleteDocumentStatusMutationVariables>(() => ({
      documentStatusId: props.document.lastStatus.id,
      documentId: props.document.id
    }))

    const close = () => {
      status.value = statuses.value[0] || null
      comment.value = ''
    }

    return {
      ErrorValidateDialogMode,
      firstActivated,
      canAdd,
      header,
      comment,
      status,
      statuses,
      statusesLoading,
      addDocumentStatusDone,
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
