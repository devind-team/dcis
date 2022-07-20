<template lang="pug">
bread-crumbs(:items="bc" fluid)
  v-card(v-if="!activeDocumentLoading")
    v-card-title {{ documentName }}
    v-card-text
      v-tabs(v-model="activeSheetIndex")
        settings-document(:document="activeDocument")
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
import { defineComponent, inject, onUnmounted, PropType, ref, useRoute } from '#app'
import { toGlobalId } from '~/services/graphql-relay'
import { useCommonQuery } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import type {
  DocumentQuery,
  DocumentQueryVariables,
  DocumentSheetQuery,
  DocumentSheetQueryVariables
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import SettingsDocument from '~/components/dcis/documents/SettingsDocument.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'
import Grid from '~/components/dcis/Grid.vue'

export default defineComponent({
  components: { BreadCrumbs, SettingsDocument, SheetControl, Grid },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const documentName = computed<string | null>(() => {
      if (!activeDocument.value) {
        return null
      }
      const division = activeDocument.value.period.multiple
        ? activeDocument.value.period.divisions
          .find(division => division.id === String(activeDocument.value.objectId))
        : null
      const version = t('dcis.grid.version', { version: activeDocument.value.version }) as string
      if (division) {
        return `${division.name}. ${version}`
      }
      return version
    })

    const bc = computed<BreadCrumbsItem[]>(() => {
      const result: BreadCrumbsItem[] = [...props.breadCrumbs]
      if (activeDocument.value) {
        result.push({
          text: activeDocument.value.period.project.name,
          to: localePath({
            name: 'dcis-projects-projectId-periods',
            params: { projectId: activeDocument.value.period.project.id }
          }),
          exact: true
        }, {
          text: activeDocument.value.period.name,
          to: localePath({
            name: 'dcis-periods-periodId-documents',
            params: { periodId: toGlobalId('PeriodType', Number(activeDocument.value.period.id)) }
          }),
          exact: true
        }, {
          text: documentName.value,
          to: localePath({
            name: 'dcis-documents-documentId',
            params: { documentId: activeDocument.value.id }
          }),
          exact: true
        })
      }
      return result
    })

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
      documentName,
      bc,
      activeSheetIndex,
      activeDocument,
      activeDocumentLoading,
      activeSheet,
      updateActiveSheet
    }
  }
})
</script>
