<template lang="pug">
v-menu(v-model="active" offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.documentUnloadMenu.buttonText') }}
  v-list(dense)
    document-unload(
      v-if="document.period.project.contentType.model === 'department'"
      :loading="loading"
      @unload-document="unloadDocument"
      @close="close"
    )
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-title {{ $t('dcis.grid.sheetMenu.documentUnloadMenu.unload') }}
    v-list-item(v-else @click="unloadDocument([])")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.documentUnloadMenu.unload') }}
</template>

<script lang="ts">
import { useMutation, MutateResult } from '@vue/apollo-composable'
import { defineComponent, PropType, ref, watch } from '#app'
import DocumentUnload, { UnloadDocumentMutationResult } from '~/components/dcis/documents/DocumentUnload.vue'
import { DocumentType, UnloadDocumentMutation, UnloadDocumentMutationVariables } from '~/types/graphql'
import unloadDocumentMutation from '~/gql/dcis/mutations/document/unload_document.graphql'

export default defineComponent({
  components: { DocumentUnload },
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    loading: { type: Boolean, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)

    const { mutate, loading, onDone } = useMutation<
      UnloadDocumentMutation,
      UnloadDocumentMutationVariables
    >(unloadDocumentMutation)
    onDone(({ data: { unloadDocument: { success, src } } }: UnloadDocumentMutationResult) => {
      if (success) {
        close()
        window.open(`/${src}`, '_blank')
      }
    })
    watch(loading, (newValue) => {
      emit('update:loading', newValue)
    })

    const unloadDocument = (additional: string[]): MutateResult<UnloadDocumentMutation> => {
      return mutate({
        documentId: props.document.id,
        additional
      })
    }

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, unloadDocument, close }
  }
})
</script>
