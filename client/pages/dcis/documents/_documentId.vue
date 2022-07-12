<template lang="pug">
v-container(fluid :key="$route.fullpath")
  template(v-if="!activeDocumentLoading")
    .title {{ activeDocument.period.name }}. {{ $t('dcis.grid.version', { version: activeDocument.version }) }}
    v-tabs.mt-1(v-model="activeSheetIndex")
      settings-document(:document-id="$route.params.documentId")
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
            v-icon mdi-cog
      v-tab(v-for="sheet in activeDocument.sheets" :key="sheet.id") {{ sheet.name }}
    v-tabs-items(v-model="activeSheetIndex")
      v-tab-item(v-for="sheet in activeDocument.sheets" :key="sheet.id")
        grid(
          v-if="activeSheet"
          :mode="GridMode.WRITE"
          :active-sheet="activeSheet"
          :update-active-sheet="updateActiveSheet"
          :active-document="activeDocument"
        )
        v-progress-circular(v-else color="primary" indeterminate)
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, inject, onUnmounted, ref, useRoute } from '#app'
import { useCommonQuery } from '~/composables'
import { GridMode } from '~/types/grid'
import type {
  DocumentQuery,
  DocumentQueryVariables,
  DocumentSheetQuery,
  DocumentSheetQueryVariables
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'
import SettingsDocument from '~/components/dcis/documents/SettingsDocument.vue'
import Grid from '~/components/dcis/Grid.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'

export default defineComponent({
  components: { SheetControl, SettingsDocument, Grid },
  setup () {
    const route = useRoute()

    const activeSheetIndex = ref<number>(0)

    const { data: activeDocument, loading: activeDocumentLoading } = useCommonQuery<
      DocumentQuery,
      DocumentQueryVariables
    >({
      document: documentQuery,
      variables: () => ({
        documentId: route.params.documentId
      })
    })
    const { data: activeSheet, update: updateActiveSheet } = useCommonQuery<
      DocumentSheetQuery,
      DocumentSheetQueryVariables
    >({
      document: documentSheetQuery,
      variables: () => ({
        documentId: route.params.documentId,
        sheetId: activeDocument.value ? activeDocument.value.sheets[activeSheetIndex.value].id : ''
      }),
      options: () => ({
        enabled: !activeDocumentLoading.value
      })
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      GridMode,
      activeSheetIndex,
      activeDocument,
      activeDocumentLoading,
      activeSheet,
      updateActiveSheet
    }
  }
})
</script>
