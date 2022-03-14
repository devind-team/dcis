<template lang="pug">
  v-container(fluid :key="$route.fullpath")
    v-card(v-if="!loading")
      v-card-title {{ doc.period.name }}. Версия: {{ doc.version }}
        v-spacer
        v-tooltip(bottom)
          template(#activator="{ on }")
            v-btn(v-on="on" @click="mutate({ documentId: $route.params.documentId })" :loading="unloadLoading" icon)
              v-icon mdi-download
          span Скачать документ
      v-tabs(v-model="active")
        v-tab(v-for="sheet in doc.sheets" :key="`key${sheet.id}`") {{ sheet.name }}
        v-tab-item(v-for="sheet in doc.sheets" :key="sheet.id")
          grid(:document-id="doc.id" :sheet="sheet" :key="`grid${sheet.id}`")
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { Ref } from '#app'
import { defineComponent, ref, useRoute, provide, inject, onUnmounted } from '#app'
import type {
  DocumentQueryVariables,
  DocumentQuery,
  UnloadDocumentMutation,
  UnloadDocumentMutationVariables
} from '~/types/graphql'
import { useCommonQuery } from '~/composables'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import unloadDocument from '~/gql/dcis/mutations/document/unload_document.graphql'
import DefaultLayout from '~/layouts/default.vue'
import Grid from '~/components/dcis/Grid.vue'

export type UnloadDocumentMutationResult = { data: UnloadDocumentMutation }

export default defineComponent({
  components: { Grid },
  setup () {
    const route = useRoute()
    const active: Ref<number> = ref<number>(0)
    const { data: doc, loading, update } = useCommonQuery<DocumentQuery, DocumentQueryVariables>({
      document: documentQuery,
      variables: () => ({
        documentId: route.params.documentId
      })
    })
    provide('documentUpdate', update)

    const { mutate, loading: unloadLoading, onDone } = useMutation<UnloadDocumentMutation, UnloadDocumentMutationVariables>(unloadDocument)
    onDone(({ data: { unloadDocument: { success, src } } }: UnloadDocumentMutationResult) => {
      if (success) {
        window.location.href = `/${src}`
      }
    })

    const layoutInstance = inject<DefaultLayout>('layoutInstance')
    layoutInstance.setFooter(false)
    onUnmounted(() => {
      layoutInstance.setFooter(true)
    })

    return {
      active,
      doc,
      loading,
      mutate,
      unloadLoading
    }
  }
})
</script>
