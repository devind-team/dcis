<template lang="pug">
v-menu(v-model="active" transition="slide-y-transition" offset-y left)
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attrs="attrs")
  v-list(dense)
    add-document(
      :can-add-any-document="period.canAddDocument"
      :user-divisions="userDivisions"
      :period="period"
      :documents="documents"
      :update="addDocumentUpdate"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content {{ $t('dcis.documents.addDocument.formText') }}
    add-document-data(
      v-if="period.canAddDocument"
      :period="period"
      :update="addDocumentUpdate"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on" )
          v-list-item-icon
            v-icon mdi-import
          v-list-item-content {{ $t('dcis.documents.addDocumentData.header') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { DataProxy } from 'apollo-cache'
import { DivisionModelType, DocumentType, PeriodType } from '~/types/graphql'
import AddDocument, { AddDocumentMutationResultType } from '~/components/dcis/documents/AddDocument.vue'
import AddDocumentData from '~/components/dcis/documents/AddDocumentData.vue'

export default defineComponent({
  components: { AddDocumentData, AddDocument },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    userDivisions: { type: Array as PropType<DivisionModelType[]>, required: true },
    addDocumentUpdate: {
      type: Function as PropType<(cache: DataProxy, result: AddDocumentMutationResultType) => void>,
      required: true
    },
    documents: { type: Array as PropType<DocumentType[]>, default: () => ([]) }
  },
  setup () {
    const active = ref<boolean>(false)
    return { active }
  }
})
</script>
