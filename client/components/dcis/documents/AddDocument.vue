<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.documents.addDocument.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.documents.addDocument.buttonText'))"
  :mutation="require('~/gql/dcis/mutations/document/add_document.graphql')"
  :variables="variables"
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
        return-object
      )
    v-alert(v-if="status && status.comment" type="warning" dense) {{ status.comment }}
    validation-provider(
      v-if="period.multiple && (canAddAnyDivisionDocument || userDivisions.length > 1)"
      v-slot="{ errors, valid }"
      :name="divisionLabel"
      rules="required"
    )
      v-autocomplete(
        v-model="division"
        :error-messages="errors"
        :success="valid"
        :items="canAddAnyDivisionDocument ? period.divisions : userDivisions"
        :label="divisionLabel"
        item-text="name"
        item-value="id"
        return-object
      )
        template(#item="{ item }")
          v-list-item-content {{ item.name }}
    v-autocomplete(
      v-if="documents.length"
      v-model="document"
      :items="documents"
      :label="$t('dcis.documents.addDocument.lastDocument')"
      :filter="documentFilter"
      item-value="id"
      success
      clearable
      return-object
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
import { computed, defineComponent, ref } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import {
  PeriodType,
  StatusType,
  DivisionModelType,
  DocumentType,
  InitialStatusesQuery,
  InitialStatusesQueryVariables,
  AddDocumentMutationPayload,
  AddDocumentMutationVariables
} from '~/types/graphql'
import initialStatusesQuery from '~/gql/dcis/queries/initial_statuses.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDocumentMutationResultType = { data: { addDocument: AddDocumentMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    canAddAnyDivisionDocument: { type: Boolean, required: true },
    userDivisions: { type: Array as PropType<DivisionModelType[]>, required: true },
    update: {
      type: Function as PropType<(cache: DataProxy, result: AddDocumentMutationResultType) => void>,
      required: true
    },
    period: { type: Object as PropType<PeriodType>, required: true },
    documents: { type: Array as PropType<DocumentType[]>, default: () => ([]) }
  },
  setup (props) {
    const { t } = useI18n()

    const divisionLabel = computed<string>(() => props.period.project.contentType.model === 'department'
      ? t('dcis.documents.addDocument.department') as string
      : t('dcis.documents.addDocument.organization') as string
    )

    const status = ref<StatusType | null>(null)
    const division = ref<DivisionModelType | null>(null)
    const document = ref<DocumentType>(null)

    const divisionId = computed<string | null>(() => {
      if (!props.period.multiple) {
        return null
      }
      if (props.canAddAnyDivisionDocument) {
        return division.value?.id
      }
      return props.userDivisions.length === 1 ? props.userDivisions[0].id : division.value?.id
    })

    const { data: statuses, onResult } = useCommonQuery<
      InitialStatusesQuery,
      InitialStatusesQueryVariables
    >({
      document: initialStatusesQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    onResult(({ data: { initialStatuses } }) => {
      nextTick(() => { status.value = initialStatuses[0] || null })
    })

    const variables = computed<AddDocumentMutationVariables>(() => ({
      periodId: props.period.id,
      statusId: status.value?.id,
      divisionId: divisionId.value,
      documentId: document.value?.id
    }))

    const close = () => {
      status.value = statuses.value[0] || null
      division.value = null
      document.value = null
    }

    const documentFilter = (item: DocumentType, queryText: string) => {
      const searchText = queryText.toLocaleLowerCase()
      return String(t('dcis.documents.addDocument.version', { version: item.version }))
        .toLocaleLowerCase()
        .includes(searchText) ||
        item.comment.toLocaleLowerCase().includes(searchText)
    }

    return {
      divisionId,
      divisionLabel,
      status,
      division,
      document,
      statuses,
      variables,
      close,
      documentFilter
    }
  }
})
</script>
