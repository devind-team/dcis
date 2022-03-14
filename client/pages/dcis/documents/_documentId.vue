<template lang="pug">
  v-container(fluid :key="$route.fullpath")
    v-card(v-if="!loading")
      v-card-title {{ doc.period.name }}. Версия: {{ doc.version }}
      v-card-subtitle {{ doc.comment }}
      v-tabs(v-model="active")
        v-tab(v-for="sheet in doc.sheets" :key="`key${sheet.id}`") {{ sheet.name }}
        v-tab-item(v-for="sheet in doc.sheets" :key="sheet.id")
          grid(:document-id="doc.id" :sheet="sheet" :key="`grid${sheet.id}`")
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, ref, useRoute, provide, inject, onUnmounted } from '#app'
import type { DocumentQueryVariables, DocumentQuery } from '~/types/graphql'
import { useCommonQuery } from '~/composables'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import Grid from '~/components/dcis/Grid.vue'
import DefaultLayout from "~/layouts/default.vue";

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

    const layoutInstance = inject<DefaultLayout>('layoutInstance')
    layoutInstance.setFooter(false)
    onUnmounted(() => {
      layoutInstance.setFooter(true)
    })

    return {
      active,
      doc,
      loading
    }
  }
})
</script>
