<template lang="pug">
  v-container(fluid)
    v-card(v-if="!loading")
      v-card-title {{ document.period.name }}. Версия: {{ document.version }}
      v-card-subtitle {{ document.comment }}
      v-tabs(v-model="active")
        v-tab(v-for="sheet in document.sheets" :key="`key${sheet.id}`") {{ sheet.name }}
        v-tab-item(v-for="sheet in document.sheets" :key="sheet.id")
          grid(:sheet="sheet")
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, ref, useRoute } from '#app'
import type { DocumentType, DocumentQueryVariables } from '~/types/graphql'
import { useCommonQuery } from '~/composables'
import GridToolbar from '~/components/dcis/GridToolbar.vue'
import Grid from '~/components/dcis/Grid.vue'

export default defineComponent({
  components: { GridToolbar, Grid },
  setup () {
    const route = useRoute()
    const active: Ref<number> = ref<number>(0)
    const { data: document, loading } = useCommonQuery<DocumentType, DocumentQueryVariables>({
      document: require('~/gql/dcis/queries/document'),
      variables: () => ({
        documentId: route.params.documentId
      })
    })

    return {
      active,
      document,
      loading
    }
  }
})
</script>
