<template lang="pug">
  mutation-modal-form(
    :mutation="require('~/gql/dcis/mutations/document/add_document.graphql')"
    :variables="variables"
    :header="String($t('dcis.documents.addDocument.header'))"
    :button-text="String($t('dcis.documents.addDocument.buttonText'))"
    :update="update"
    mutation-name="addDocument"
    i18n-path="dcis.documents.addDocument"
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String($t('dcis.documents.addDocument.comment'))"
        rules="required"
      )
        v-text-field(
          v-model="comment"
          :error-messages="errors"
          :success="valid"
          :label="$t('dcis.documents.addDocument.comment')"
          autofocus
        )
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String($t('dcis.documents.addDocument.status'))"
        rules="required"
      )
        v-select(
          v-model="status"
          :error-messages="errors"
          :success="valid"
          :items="statuses"
          :label="$t('dcis.documents.addDocument.status')"
          item-text="name"
          item-value="id"
        )
      v-autocomplete(
        v-if="documents.length"
        v-model="document"
        :items="documents"
        :label="$t('dcis.documents.addDocument.lastDocument')"
        :filter="documentFilter"
        item-value="id"
        success
        clearable
      )
        template(#selection="{ item }") {{ $t('dcis.documents.addDocument.version', { version: item.version }) }}
        template(#item="{ item }")
          v-list-item-content
            v-list-item-title {{ $t('dcis.documents.addDocument.version', { version: item.version }) }}
            v-list-item-subtitle {{ item.comment }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { useCommonQuery } from '~/composables'
import {
  PeriodType,
  DocumentType,
  StatusType,
  StatusesQuery,
  StatusesQueryVariables,
  AddDocumentMutationPayload,
  AddDocumentMutationVariables
} from '~/types/graphql'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentMutationResultType = { data: { addDocument: AddDocumentMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    update: {
      type: Function as PropType<(cache: DataProxy, result: AddDocumentMutationResultType) => void>,
      required: true
    },
    period: { type: Object as PropType<PeriodType>, required: true },
    documents: { type: Array as PropType<DocumentType[]>, default: () => ([]) }
  },
  setup (props) {
    const { t } = useI18n()

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
      periodId: Number(props.period.id),
      statusId: Number(status.value?.id),
      documentId: document.value?.id
    }))

    const close = () => {
      comment.value = ''
      status.value = statuses[0]
      document.value = null
    }

    const documentFilter = (item: DocumentType, queryText: string) => {
      const searchText = queryText.toLocaleLowerCase()
      return String(t('dcis.documents.addDocument.version', { version: item.version }))
        .toLocaleLowerCase()
        .includes(searchText) ||
        item.comment.toLocaleLowerCase().includes(searchText)
    }

    return { comment, status, document, statuses, variables, close, documentFilter }
  }
})
</script>
