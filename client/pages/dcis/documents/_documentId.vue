<template lang="pug">
  v-container(fluid)
    v-card(v-if="!loading")
      v-card-title {{ doc.period.name }}. Версия: {{ doc.version }}
      v-card-subtitle {{ doc.comment }}
      v-tabs(v-model="active")
        v-tab(v-for="sheet in doc.sheets" :key="`key${sheet.id}`") {{ sheet.name }}
        v-tab-item(v-for="sheet in doc.sheets" :key="sheet.id")
          grid(:document-id="doc.id" :sheet="sheet")
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, ref, useRoute, provide } from '#app'
import type { DocumentQueryVariables, DocumentQuery } from '~/types/graphql'
import { useCommonQuery } from '~/composables'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import GridToolbar from '~/components/dcis/GridToolbar.vue'
import Grid from '~/components/dcis/Grid.vue'

export default defineComponent({
  components: { GridToolbar, Grid },
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

    return {
      active,
      doc,
      loading
    }
  }
})
</script>
