<template lang="pug">
  v-container
    v-card(v-if="!loading")
      v-card-text
        pre {{ document }}
</template>

<script lang="ts">
import { defineComponent, useRoute } from '#app'
import type { DocumentType, DocumentQueryVariables } from '~/types/graphql'
import { useCommonQuery } from '~/composables'
import GridToolbar from '~/components/dcis/GridToolbar.vue'
import Grid from '~/components/dcis/Grid.vue'

export default defineComponent({
  components: { GridToolbar, Grid },
  setup () {
    const route = useRoute()
    const { data: document, loading } = useCommonQuery<DocumentType, DocumentQueryVariables>({
      document: require('~/gql/dcis/queries/document'),
      variables: () => ({
        documentId: route.params.documentId
      })
    })

    return {
      document,
      loading
    }
  }
})
</script>
