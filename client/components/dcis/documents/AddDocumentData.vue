<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.documents.addDocumentData.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.documents.addDocumentData.buttonText'))"
  :mutation="require('~/gql/dcis/mutations/document/add_document_data.graphql')"
  :variables="variables"
  :update="update"
  mutation-name="addDocumentData"
  i18n-path="dcis.documents.addDocumentData"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.documents.addDocumentData.file'))" rules="required")
      v-file-input(
        v-model="file"
        :label="String($t('dcis.documents.addDocumentData.file'))"
        :error-messages="errors"
        :success="valid"
        placeholder="Выберете файл"
        hint="Файл в формате xlsx"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        persistent-hint clearable
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.documents.addDocumentData.status'))"
      rules="required"
    )
      v-select(
        v-model="status"
        :error-messages="errors"
        :success="valid"
        :items="statuses"
        :label="$t('dcis.documents.addDocumentData.status')"
        item-text="name"
        item-value="id"
        return-object
      )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, ref, computed, unref, PropType } from '#app'
import { useCommonQuery } from '~/composables'
import {
  AddDocumentDataMutationInput,
  AddDocumentDataMutationPayload,
  PeriodType,
  InitialStatusesQuery,
  InitialStatusesQueryVariables,
  StatusType
} from '~/types/graphql'
import initialStatusesQuery from '~/gql/dcis/queries/initial_statuses.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentsDataMutationsResultType = { data: { addDocumentData: AddDocumentDataMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: {
      type: Function as PropType<(cache: DataProxy, result: AddDocumentsDataMutationsResultType) => void>,
      required: true
    }
  },
  setup (props) {
    const file = ref<File | null>(null)
    const status = ref<StatusType | null>(null)
    const comment = ref<string>('')

    const { data: statuses } = useCommonQuery<InitialStatusesQuery, InitialStatusesQueryVariables>({
      document: initialStatusesQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    const variables = computed<AddDocumentDataMutationInput>(() => ({
      periodId: props.period.id,
      file: unref(file),
      statusId: unref(status)?.id,
      comment: unref(comment)
    }))

    const close = () => {
      file.value = null
      status.value = null
      comment.value = ''
    }

    return {
      file,
      comment,
      status,
      statuses,
      variables,
      close
    }
  }
})
</script>
