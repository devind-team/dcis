<template lang="pug">
  mutation-modal-form(
    :header="$t('dcis.documents.status.header')"
    :subheader="`Версия ${document.version}`"
    :button-text="$t('dcis.documents.status.buttonText')"
    :mutation="addDocumentStatus"
    :variables="{ documentId: document.id, userId: user.id, statusId: status.id, comment }"
    :update="addDocumentStatusUpdate"
    mutation-name="addDocumentStatus"
    i18n-path="dcis.documents.status"
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
        template(v-for="(item, index) in docStatuses")
          v-list-item(v-if="item.document.id === document.id" :key="item.id")
            v-list-item-content
              v-list-item-title {{ item.status.name }}
              v-list-item-subtitle {{ dateTimeHM(item.createdAt) }}
              v-list-item-subtitle {{ $getUserName(item.user) }}
            v-list-item-content
              v-list-item-subtitle.font-italic {{ item.comment }}
            v-list-item-action
              v-btn(v-if="docStatuses.filter(e => e.document.id === document.id).length > 1" @click="deleteStatus(item)" icon)
                v-icon(color="error") mdi-close-circle
          v-divider(v-if="item.document.id === document.id" :key="index")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType, Ref } from '#app'
import { defineComponent, ref } from '#app'
import {
  AddDocumentStatusMutationPayload,
  DocumentStatusType,
  DocumentType,
  StatusType,
  UserType
} from '~/types/graphql'
import addDocumentStatus from '~/gql/dcis/mutations/document/add_status.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useFilters } from '~/composables'

export type AddDocumentStatusMutationResult = { data: { addDocumentStatus: AddDocumentStatusMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddDocumentStatusMutationPayload | any) => DataProxy | void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    user: { type: Object as PropType<UserType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true },
    statuses: { type: Array as PropType<StatusType[]>, required: true },
    docStatuses: { type: Array as PropType<DocumentStatusType[]>, default: () => [], required: true },
    deleteStatus: { type: Function as PropType<Function>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()
    const comment: Ref<string> = ref<string>('')
    const status: Ref<StatusType> = ref<StatusType>(props.document.lastStatus.status)
    const addDocumentStatusUpdate = (cache: DataProxy, result: AddDocumentStatusMutationResult) => {
      const { success } = result.data.addDocumentStatus
      if (success) {
        props.update(cache, result)
      }
    }
    const close = () => {
      status.value = props.document.lastStatus.status
      comment.value = ''
    }
    return { comment, status, addDocumentStatusUpdate, addDocumentStatus, dateTimeHM, close }
  }
})
</script>
