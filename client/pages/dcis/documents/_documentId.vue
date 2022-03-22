<template lang="pug">
  v-container(fluid :key="$route.fullpath")
    template(v-if="!loading")
      .title {{ doc.period.name }}. Версия: {{ doc.version }}
      v-tabs.mt-1(v-model="active")
        v-menu(bottom left)
          template(#activator="{ on, attrs }")
            v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
              v-icon mdi-cog
          v-list
            v-list-item(@click="mutate({ documentId: $route.params.documentId })")
              v-list-item-icon
                v-icon mdi-download
              v-list-item-content
                v-list-item-title Скачать документ
        v-tab(v-for="sheet in doc.sheets" :key="`key${sheet.id}`") {{ sheet.name }}
      v-tabs-items(v-model="active")
        v-tab-item(v-for="sheet in doc.sheets" :key="sheet.id")
          grid.mt-1(:document-id="doc.id" :sheet="sheet" :update="update" :key="`grid${sheet.id}`")
    v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { Ref } from '#app'
import { defineComponent, ref, useRoute, inject, onUnmounted } from '#app'
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

    return { active, doc, loading, mutate, unloadLoading, update }
  }
})
</script>
