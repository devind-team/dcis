<template lang="pug">
  v-dialog(v-model="active" width="600")
    template(#activator="{ on, attrs }")
      slot(name="activator" :on="on" :attrs="attrs")
    v-card
      v-card-title {{ $t('dcis.documents.unloading.name') }}
        v-spacer
        v-btn(@click="close" icon)
          v-icon mdi-close
      v-card-subtitle {{ $t('dcis.documents.unloading.additional') }}
      v-card-text
        v-checkbox(
          v-for="param in params"
          v-model="additional"
          :key="param"
          :label="$t(`dcis.documents.unloading.${param}`)"
          :value="param"
          dense
        )
      v-card-actions
        v-spacer
        v-btn(@click="mutate({ documentId, additional })" :loading="loading" color="primary") {{ $t('dcis.documents.unloading.unload') }}
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { UnloadDocumentMutation, UnloadDocumentMutationVariables } from '~/types/graphql'
import unloadDocument from '~/gql/dcis/mutations/document/unload_document.graphql'

export type UnloadDocumentMutationResult = { data: UnloadDocumentMutation }

export default defineComponent({
  props: {
    documentId: { type: String, required: true }
  },
  setup (_, { emit }) {
    const active = ref<boolean>(false)
    const params: string[] = ['rowAddDate', 'rowUpdateDate', 'divisionName', 'divisionHeader', 'user']
    const additional = ref<string[]>(params)
    const { mutate, loading, onDone } = useMutation<UnloadDocumentMutation, UnloadDocumentMutationVariables>(unloadDocument)
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
    return { active, mutate, loading, params, additional, close }
  }
})
</script>
