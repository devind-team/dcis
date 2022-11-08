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
import {
  AttributesQuery,
  AttributesQueryVariables,
  AttributesValuesQuery, AttributesValuesQueryVariables,
  DocumentQuery,
  DocumentQueryVariables
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import attributesQuery from "~/gql/dcis/queries/attributes.graphql";
import attributesValuesQuery from "~/gql/dcis/queries/attributes_values.graphql";

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

    return { bc }
  }
})
</script>
