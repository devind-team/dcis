<template lang="pug">
left-navigator-container.document-sheets__left-navigator-container(
  :bread-crumbs="breadCrumbs"
  fluid
  @update-drawer="$emit('update-drawer')"
)
  template(#subheader) {{ document.objectName }}
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="mode"
    :sheets="document.sheets"
    :active-sheet="activeSheet"
    :update-active-sheet="updateActiveSheet"
    :active-document="document"
  )
    template(#menus)
      document-unload-menu(:document="document")
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useCommonQuery } from '~/composables'
import {
  DocumentSheetQuery,
  DocumentSheetQueryVariables,
  DocumentType
} from '~/types/graphql'
import { GridMode } from '~/types/grid'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import DocumentUnloadMenu from '~/components/dcis/grid/menus/DocumentUnloadMenu.vue'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs, GridSheets, DocumentUnloadMenu },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> },
    document: { type: Object as PropType<DocumentType>, required: true }
  },
  setup (props) {
    const activeSheetIndex = ref<number>(0)

    const mode = computed<GridMode>(
      () => props.document.lastStatus.status.edit ? GridMode.WRITE : GridMode.READ
    )

    const { data: activeSheet, loading: activeSheetLoading, update: updateActiveSheet } = useCommonQuery<
      DocumentSheetQuery,
      DocumentSheetQueryVariables
    >({
      document: documentSheetQuery,
      variables: () => ({
        documentId: props.document.id,
        sheetId: props.document.sheets[activeSheetIndex.value]?.id
      }),
      options: () => ({
        fetchPolicy: 'cache-and-network'
      })
    })

    return {
      activeSheetIndex,
      mode,
      activeSheet,
      activeSheetLoading,
      updateActiveSheet
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
