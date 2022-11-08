<template lang="pug">
bread-crumbs(:items="bc" fluid)
  v-card(v-if="!activeDocumentLoading")
    v-card-subtitle {{ activeDocument.objectName }}
    v-card-text
      grid-sheets(
        v-model="activeSheetIndex"
        :mode="GridMode.WRITE"
        :sheets="activeDocument.sheets"
        :active-sheet="activeSheet"
        :update-active-sheet="updateActiveSheet"
        :active-document="activeDocument"
        show-attributes
      )
        template(#settings)
          settings-document(:document="activeDocument")
            template(#activator="{ on, attrs }")
              v-btn(v-on="on" v-bind="attrs" class="align-self-center mr-4" icon text)
                v-icon mdi-cog
        template(#attributes)
          attributes-values-tab-item(
            :document-id="activeDocument.id"
            :loading="attributesLoading || attributesValuesLoading"
            :attributes="attributes"
            :attributes-values="attributesValues"
            :readonly="!activeDocument.canChangeAttributeValue"
            :change-update-attributes-values="changeUpdateAttributesValues"
            :update-active-sheet="updateActiveSheet"
          )
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, inject, onUnmounted, PropType, ref, useRoute } from '#app'
import { toGlobalId } from '~/services/graphql-relay'
import { useCommonQuery, useI18n } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import type {
  AttributesQuery,
  AttributesQueryVariables,
  AttributesValuesQuery,
  AttributesValuesQueryVariables,
  DocumentQuery,
  DocumentQueryVariables,
  DocumentSheetQuery,
  DocumentSheetQueryVariables
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'
import attributesQuery from '~/gql/dcis/queries/attributes.graphql'
import attributesValuesQuery from '~/gql/dcis/queries/attributes_values.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import SettingsDocument from '~/components/dcis/documents/SettingsDocument.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import AttributesValuesTabItem from '~/components/dcis/attributes/AttributesValuesTabItem.vue'

export default defineComponent({
  components: { AttributesValuesTabItem, BreadCrumbs, SettingsDocument, SheetControl, GridSheets },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const documentVersion = computed<string>(() =>
      t('dcis.grid.version', { version: activeDocument.value.version }) as string)

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
          text: documentVersion.value,
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
    const { data: activeSheet, loading: activeSheetLoading, update: updateActiveSheet } = useCommonQuery<
      DocumentSheetQuery,
      DocumentSheetQueryVariables
    >({
      document: documentSheetQuery,
      variables: () => ({
        documentId: route.params.documentId,
        // activeSheetIndex.value - 1 - 0 индекс принадлежит атрибутам
        sheetId: activeDocument.value?.sheets[activeSheetIndex.value - 1]?.id
      }),
      options: () => ({
        enabled: !activeDocumentLoading.value && !!activeDocument.value?.sheets[activeSheetIndex.value - 1]?.id,
        fetchPolicy: 'cache-and-network'
      })
    })

    const { data: attributes, loading: attributesLoading } = useCommonQuery<AttributesQuery, AttributesQueryVariables>({
      document: attributesQuery,
      variables: () => ({ periodId: activeDocument.value?.period.id }),
      options: () => ({ enabled: !activeDocumentLoading.value })
    })

    const { data: attributesValues, loading: attributesValuesLoading, changeUpdate: changeUpdateAttributesValues } = useCommonQuery<
      AttributesValuesQuery,
      AttributesValuesQueryVariables
    >({
      document: attributesValuesQuery,
      variables: () => ({ documentId: route.params.documentId }),
      options: () => ({ enabled: !activeDocumentLoading.value })
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      GridMode,
      bc,
      activeSheetIndex,
      activeDocument,
      activeDocumentLoading,
      activeSheet,
      activeSheetLoading,
      updateActiveSheet,
      attributes,
      attributesLoading,
      attributesValues,
      attributesValuesLoading,
      changeUpdateAttributesValues
    }
  }
})
</script>
