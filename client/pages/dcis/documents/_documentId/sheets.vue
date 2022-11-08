<template lang="pug">
div
  left-navigator-container(v-if="!activeDocumentLoading" :bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
    v-card-subtitle {{ activeDocument.objectName }}
    v-card-text
      grid-sheets(
        v-model="activeSheetIndex"
        :mode="GridMode.WRITE"
        :sheets="activeDocument.sheets"
        :active-sheet="activeSheet"
        :update-active-sheet="updateActiveSheet"
        :active-document="activeDocument"
      )
        template(#settings)
          settings-document(:document="activeDocument")
            template(#activator="{ on, attrs }")
              v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
                v-icon mdi-cog
  v-progress-circular(color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, PropType, ref, useRoute } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import SettingsDocument from '~/components/dcis/documents/SettingsDocument.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import { useCommonQuery } from '~/composables'
import { DocumentQuery, DocumentQueryVariables, DocumentSheetQuery, DocumentSheetQueryVariables } from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import { GridMode } from '~/types/grid'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs, SettingsDocument, SheetControl, GridSheets },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
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

    const { data: activeSheet, loading: activeSheetLoading, update: updateActiveSheet } = useCommonQuery<
      DocumentSheetQuery,
      DocumentSheetQueryVariables
    >({
      document: documentSheetQuery,
      variables: () => ({
        documentId: route.params.documentId,
        sheetId: activeDocument.value?.sheets[activeSheetIndex.value]?.id
      }),
      options: () => ({
        enabled: !activeDocumentLoading.value && !!activeDocument.value?.sheets[activeSheetIndex.value]?.id,
        fetchPolicy: 'cache-and-network'
      })
    })

    return {
      GridMode,
      activeSheetIndex,
      activeDocument,
      activeDocumentLoading,
      activeSheet,
      activeSheetLoading,
      updateActiveSheet
    }
  }
})
</script>
