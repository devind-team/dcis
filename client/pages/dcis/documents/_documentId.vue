<template lang="pug">
  v-container(fluid :key="$route.fullpath")
    template(v-if="!activeDocumentLoading")
      .title {{ activeDocument.period.name }}. {{ t('dcis.grid.version', { version: activeDocument.version }) }}
      v-tabs.mt-1(v-model="active")
        settings-document(:document-id="$route.params.documentId")
          template(#activator="{ on, attrs }")
            v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
              v-icon mdi-cog
        v-tab(v-for="sheet in activeDocument.sheets" :key="`key${sheet.id}`") {{ sheet.name }}
      v-tabs-items(v-model="active")
        v-tab-item(v-for="sheet in activeDocument.sheets" :key="sheet.id")
          grid(v-if="!activeSheetLoading && activeSheet")
          v-progress-circular(v-else color="primary" indeterminate)
    v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import type {
  DocumentQuery,
  DocumentQueryVariables,
  SheetQuery,
  SheetQueryVariables
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import sheetQuery from '~/gql/dcis/queries/sheet.graphql'
import SettingsDocument from '~/components/dcis/documents/SettingsDocument.vue'
import Grid from '~/components/dcis/Grid.vue'

export default defineComponent({
  components: { SettingsDocument, Grid },
  setup () {
    const { t } = useI18n()
    const route = useRoute()

    const active = ref<number>(0)

    const { data: activeDocument, loading: activeDocumentLoading } = useCommonQuery<
      DocumentQuery,
      DocumentQueryVariables
    >({
      document: documentQuery,
      variables: () => ({
        documentId: route.params.documentId
      })
    })
    const { data: activeSheet, loading: activeSheetLoading, update: updateActiveSheet } = useCommonQuery<
      SheetQuery,
      SheetQueryVariables
    >({
      document: sheetQuery,
      variables: () => ({
        documentId: route.params.documentId,
        sheetId: activeDocumentLoading.value ? '' : activeDocument.value.sheets[active.value].id
      }),
      options: () => ({
        enabled: !activeDocumentLoading.value
      })
    })

    provide('activeDocument', activeDocument)
    provide('activeSheet', activeSheet)
    provide('updateActiveSheet', updateActiveSheet)

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      t,
      active,
      activeDocument,
      activeDocumentLoading,
      activeSheet,
      activeSheetLoading
    }
  }
})
</script>
