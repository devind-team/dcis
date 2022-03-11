<template lang="pug">
  v-container
    v-card
      grid-toolbar(v-model="activeSheet" :document="document")
      v-card-text
        grid(:sheet="activeSheet")
</template>

<script lang="ts">
import { defineComponent, computed, useRoute } from '#app'
import type { ComputedRef } from '#app'
import type { DocumentType, SheetType, DocumentQueryVariables } from '~/types/graphql'
import { useCommonQuery } from '~/composables'
import GridToolbar from '~/components/dcis/GridToolbar.vue'
import Grid from '~/components/dcis/Grid.vue'

export default defineComponent({
  components: { GridToolbar, Grid },
  setup () {
    const route = useRoute()
    const { data: document } = useCommonQuery<DocumentType, DocumentQueryVariables>({
      document: require('~/gql/dcis/queries/document'),
      variables: () => ({
        documentId: route.params.documentId
      })
    })

    const activeSheet: ComputedRef<SheetType> = computed<SheetType>(() =>
      document.value && document.value.sheets.length ? document.value.sheets[0] : null
    )

    return {
      activeSheet,
      document
    }
  }
})
</script>
