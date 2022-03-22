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
    @done="done"
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
      validation-provider(
        v-slot="{ errors, valid }"
        :name="$t('dcis.documents.status.comment')"
        rules="required|min:3|max:250"
      )
        v-text-field(
          v-model="comment"
          :label="$t('dcis.documents.status.comment')"
          :error-messages="errors"
          :success="valid"
        )
      v-list(two-line dense)
        template(v-for="(status, index) in document.statuses")
          v-list-item(:key="status.id")
            v-list-item-content
              v-list-item-title {{ status.status.name }}
              v-list-item-subtitle {{ $filters.dateTimeHM(status.createdAt) }}
              v-list-item-subtitle {{ $getUserName(status.user) }}
            v-list-item-content
              v-list-item-subtitle.font-italic {{ status.comment }}
            v-list-item-action
              v-btn(@click="mutate" icon)
                v-icon(color="error") mdi-close-circle
          v-divider(v-if="index < document.statuses.length - 1" :key="index")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType, Ref } from '#app'
import { defineComponent, ref } from '#app'
import {
  AddDocumentStatusMutationPayload,
  DocumentType,
  StatusType,
  UserType
} from '~/types/graphql'
import addDocumentStatus from '~/gql/dcis/mutations/document/add_status.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentStatusMutationResult = { data: { addDocumentStatus: AddDocumentStatusMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddDocumentStatusMutationPayload | any) => DataProxy | void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    user: { type: Object as PropType<UserType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true },
    statuses: { type: Array as PropType<any>, required: true }
  },
  setup (props) {
    const comment: Ref<string> = ref<string>('')
    const status: Ref<StatusType> = ref<StatusType>(props.document.lastStatus.status)
    const addDocumentStatusUpdate = (cache: DataProxy, result: AddDocumentStatusMutationResult) => {
      const { success } = result.data.addDocumentStatus
      if (success) {
        props.update(cache, result)
      }
    }
    return { comment, status, addDocumentStatusUpdate, addDocumentStatus }
  }
})
</script>
