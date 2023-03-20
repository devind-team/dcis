<template lang="pug">
  left-navigator-container(
    v-if="!activeDocumentLoading"
    :bread-crumbs="bc"
    fluid
    @update-drawer="$emit('update-drawer')"
  )
    template(#subheader) {{ activeDocument.objectName }}
    grid-sheets(
      v-model="activeSheetIndex"
      :mode="GridMode.READ"
      :sheets="activeDocument.sheets"
      :active-sheet="activeSheet"
      :update-active-sheet="updateActiveSheet"
      :active-document="activeDocument"
      :loading="activeDocumentLoading"
    )
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed, useRoute } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import { useCommonQuery, useI18n } from '~/composables'
import {
  DocumentQuery,
  DocumentQueryVariables,
  DocumentSheetQuery,
  DocumentSheetQueryVariables,
  DocumentsQuery,
  DocumentsQueryVariables,
  DocumentType,
  PeriodType
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import { GridMode } from '~/types/grid'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs, GridSheets },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()
    const route = useRoute()

    const activeSheetIndex = ref<number>(0)
    const { data: documents } = useCommonQuery<
      DocumentsQuery,
      DocumentsQueryVariables
    >({
      document: documentsQuery,
      variables: () => ({
        periodId: route.params.archiveId,
        divisionIds: [],
        lastStatusIds: []
      })
    })

    const doc = computed<DocumentType | null>(() => documents.value ? documents.value[0] : null)

    const { data: activeDocument, loading: activeDocumentLoading } = useCommonQuery<
      DocumentQuery,
      DocumentQueryVariables
    >({
      document: documentQuery,
      variables: () => ({
        documentId: doc.value?.id
      }),
      options: () => ({
        enabled: !doc.value
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

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: 'Документ',
        to: localePath({ name: 'dcis-periods-archive-archiveId-document_sheets' }),
        exact: true
      }
    ]))

    return {
      bc,
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
