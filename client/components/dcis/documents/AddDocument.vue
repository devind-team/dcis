<template lang="pug">
mutation-modal-form(
  @close="close"
  :mutation="require('~/gql/dcis/mutations/document/add_document.graphql')"
  :variables="variables"
  :header="String($t('dcis.documents.add.header'))"
  :button-text="String($t('add'))"
  :update="update"
  i18n-path="dcis.documents.add"
  mutation-name="addDocument"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(:name="String($t('dcis.documents.add.comment'))" rules="required" v-slot="{ errors, valid }")
      v-text-field(v-model="comment" :error-messages="errors" :success="valid" :label="$t('dcis.documents.add.comment')" autofocus)
    validation-provider(:name="String($t('dcis.documents.add.status'))" rules="required" v-slot="{ errors, valid }")
      v-combobox(v-model="status" :items="statuses" :label="$t('dcis.documents.add.status')" item-text="name" item-value="id")
    v-combobox(v-if="documents.length" v-model="document" :items="documents" :label="$t('dcis.documents.add.lastDocument')" clearable)
      template(#selection="{ item }") Версия {{ item.version }}
      template(#item="{ item }")
        v-list-item-content
          v-list-item-title Версия {{ item.version }}
          v-list-item-subtitle {{ item.comment }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { useCommonQuery } from '~/composables'
import {
  AddDocumentMutationPayload, AddDocumentMutationVariables,
  PeriodType,
  StatusesQuery,
  StatusesQueryVariables,
  StatusType
} from '~/types/graphql'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentMutationResultType = { data: { addDocument: AddDocumentMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    update: { type: Function as PropType<(cache: DataProxy, result: AddDocumentMutationResultType) => void>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    documents: { type: Array as PropType<DocumentType>, default: () => ([]) }
  },
  setup (props) {
    const comment = ref<string>('')
    const status = ref<StatusType | null>(null)
    const document = ref<DocumentType>(null)

    const { data: statuses, onResult } = useCommonQuery<StatusesQuery, StatusesQueryVariables>({
      document: statusesQuery
    })
    onResult(({ data: { statuses } }) => {
      status.value = statuses[0]
    })

    const variables = computed<AddDocumentMutationVariables>(() => ({
      comment: comment.value,
      periodId: props.period.id,
      statusId: status.value?.id,
      documentId: document.value?.id
    }))

    const close = () => {
      comment.value = ''
      status.value = statuses[0]
    }

    return { comment, status, document, statuses, variables, close }
  }
})
</script>
