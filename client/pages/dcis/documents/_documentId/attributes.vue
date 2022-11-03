<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.documents.links.attributes') }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, useRoute } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { toGlobalId } from '~/services/graphql-relay'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AttributesValuesTabItem from '~/components/dcis/attributes/AttributesValuesTabItem.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import SettingsDocument from '~/components/dcis/documents/SettingsDocument.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import { useCommonQuery, useI18n } from '~/composables'
import { DocumentQuery, DocumentQueryVariables } from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, AttributesValuesTabItem, BreadCrumbs, SettingsDocument, SheetControl, GridSheets },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const { data: activeDocument } = useCommonQuery<
      DocumentQuery,
      DocumentQueryVariables
    >({
      document: documentQuery,
      variables: () => ({
        documentId: route.params.documentId
      })
    })
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
    return { bc }
  }
})
</script>
