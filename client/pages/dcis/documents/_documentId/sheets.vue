<template lang="pug">
left-navigator-container.document-sheets__left-navigator-container(
  v-if="!activeDocumentLoading"
  :bread-crumbs="breadCrumbs"
  fluid
  @update-drawer="$emit('update-drawer')"
)
  template(#subheader) {{ activeDocument.objectName }}
  full-screen-in-place(:is-full-screen="view.isFullScreen")
    grid-sheets(
      v-model="activeSheetIndex"
      :mode="mode"
      :is-full-screen="view.isFullScreen"
      :sheets="activeDocument.sheets"
      :active-sheet="activeSheet"
      :update-active-sheet="updateActiveSheet"
      :active-document="activeDocument"
      :loading="activeDocumentLoading"
    )
      template(#menus="{ selectedCellsOptions }")
        edit-menu(:mode="mode" :selected-cells-options="selectedCellsOptions")
        document-unload-menu(:document="activeDocument")
        view-menu(v-model="view")
v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref, useRoute } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useCommonQuery } from '~/composables'
import { DocumentQuery, DocumentQueryVariables, DocumentSheetQuery, DocumentSheetQueryVariables } from '~/types/graphql'
import { GridMode } from '~/types/grid'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import FullScreenInPlace from '~/components/common/FullScreenInPlace.vue'
import EditMenu from '~/components/dcis/grid/menus/EditMenu.vue'
import ViewMenu, { ViewType } from '~/components/dcis/grid/menus/ViewMenu.vue'
import DocumentUnloadMenu from '~/components/dcis/grid/menus/DocumentUnloadMenu.vue'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    BreadCrumbs,
    FullScreenInPlace,
    GridSheets,
    EditMenu,
    ViewMenu,
    DocumentUnloadMenu
  },
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

    const view = ref<ViewType>({ isFullScreen: false })

    return {
      activeSheetIndex,
      activeDocument,
      activeDocumentLoading,
      mode,
      activeSheet,
      activeSheetLoading,
      updateActiveSheet,
      view
    }
  }
})
</script>

<style lang="sass">
.document-sheets__left-navigator-container
  position: relative
  z-index: 0

  .v-card__subtitle
    padding-bottom: 8px
</style>
