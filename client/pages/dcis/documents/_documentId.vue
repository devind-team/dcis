<template lang="pug">
  v-container(fluid :key="$route.fullpath")
    template(v-if="!activeDocumentLoading")
      .title {{ activeDocument.period.name }}. {{ t('dcis.grid.version', { version: activeDocument.version }) }}
      v-tabs.mt-1(v-model="active")
        settings-document(:document-id="$route.params.documentId")
          template(#activator="{ on, attrs }")
            v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
              v-icon mdi-cog
        v-tab(v-for="sh in activeDocument.sheets" :key="`key${sh.id}`")
          sheet-control(v-slot="{ on, attrs }" :sheet="sh" :update="changeUpdate")
            div(v-bind="attrs" @contextmenu.prevent="on.click") {{ sh.name }}
      v-tabs-items(v-model="active")
        v-tab-item(v-for="sheet in activeDocument.sheets" :key="sheet.id")
          grid(
            v-if="!activeSheetLoading && activeSheet"
            :active-sheet="activeSheet"
            :update-active-sheet="updateActiveSheet"
            :active-document="activeDocument"
          )
          v-progress-circular(v-else color="primary" indeterminate)
    v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, inject, onUnmounted, ref, useRoute } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
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
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'

export default defineComponent({
  components: { SheetControl, SettingsDocument, Grid },
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
    const { data: activeSheet, loading: activeSheetLoading, update: updateActiveSheet, changeUpdate } = useCommonQuery<
      SheetQuery,
      SheetQueryVariables
    >({
      document: sheetQuery,
      variables: () => ({
        documentId: route.params.documentId,
        sheetId: activeDocumentLoading.value ? undefined : activeDocument.value.sheets[active.value].id
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
      t,
      active,
      activeDocument,
      activeDocumentLoading,
      activeSheet,
      activeSheetLoading,
      updateActiveSheet,
      changeUpdate
    }
  }
})
</script>
