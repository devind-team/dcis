<template lang="pug">
left-navigator-container(
  v-if="!activeDocumentLoading"
  :bread-crumbs="breadCrumbs"
  fluid
  @update-drawer="$emit('update-drawer')"
)
  template(#subheader) {{ activeDocument.objectName }}
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="mode"
    :sheets="activeDocument.sheets"
    :active-sheet="activeSheet"
    :update-active-sheet="updateActiveSheet"
    :active-document="activeDocument"
    :loading="activeDocumentLoading"
  )
    template(#settings)
      settings-document(:document="activeDocument")
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
            v-icon mdi-cog
v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref, useRoute } from '#app'
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

    const mode = computed<GridMode>(
      () => activeDocument.value.lastStatus.status.edit ? GridMode.WRITE : GridMode.READ
    )

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
      activeSheetIndex,
      activeDocument,
      activeDocumentLoading,
      mode,
      activeSheet,
      activeSheetLoading,
      updateActiveSheet
    }
  }
})
</script>
