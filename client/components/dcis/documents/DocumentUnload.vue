<template lang="pug">
v-dialog(v-model="active" width="600")
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-card
    v-card-title {{ $t('dcis.documents.unloadDocument.name') }}
      v-spacer
      v-btn(@click="close" icon)
        v-icon mdi-close
    v-card-subtitle {{ $t('dcis.documents.unloadDocument.additional') }}
    v-card-text
      v-checkbox(
        v-for="param in params"
        v-model="additional"
        :key="param"
        :label="paramsTranslations[param]"
        :value="param"
        dense
      )
    v-card-actions
      v-spacer
      v-btn(
        :loading="loading"
        color="primary"
        @click="mutate({ documentId: document.id, additional })"
      ) {{ $t('dcis.documents.unloadDocument.unload') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { DocumentType, UnloadDocumentMutation, UnloadDocumentMutationVariables } from '~/types/graphql'
import unloadDocument from '~/gql/dcis/mutations/document/unload_document.graphql'

export type UnloadDocumentMutationResult = { data: UnloadDocumentMutation }

export default defineComponent({
  props: {
    document: { type: Object as PropType<DocumentType>, required: true }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const active = ref<boolean>(false)

    const params: string[] = ['row_add_date', 'row_update_date', 'division_name', 'division_head', 'user']
    const additional = ref<string[]>([])

    const paramsTranslations = computed<Record<string, string>>(() => ({
      row_add_date: t('dcis.documents.unloadDocument.rowAddDate') as string,
      row_update_date: t('dcis.documents.unloadDocument.rowUpdateDate') as string,
      division_name: props.document.period.project.contentType.model === 'department'
        ? t('dcis.documents.unloadDocument.departmentName') as string
        : t('dcis.documents.unloadDocument.organizationName') as string,
      division_head: props.document.period.project.contentType.model === 'department'
        ? t('dcis.documents.unloadDocument.departmentHead') as string
        : t('dcis.documents.unloadDocument.organizationHead') as string,
      user: t('dcis.documents.unloadDocument.user') as string
    }))

    const { mutate, loading, onDone } = useMutation<
      UnloadDocumentMutation,
      UnloadDocumentMutationVariables
    >(unloadDocument)
    onDone(({ data: { unloadDocument: { success, src } } }: UnloadDocumentMutationResult) => {
      if (success) {
        close()
        window.location.href = `/${src}`
      }
    })

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, params, additional, paramsTranslations, mutate, loading, close }
  }
})
</script>
