<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(v-if="!loading")
    template(v-if="attributes.length")
      component(
        v-for="attribute in attributes"
        :key="attribute.id"
        :is="AttributeValueComponents[attribute.kind]"
        :attribute="attribute"
        :attribute-value="attribute.id in attributesValues ? attributesValues[attribute.id] : null"
        :readonly="true"
      )
    v-alert(v-else type="info") {{ $t('dcis.documents.attributes.noAttributes') }}
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, useRoute, PropType } from '#app'
import {
  AttributesQuery,
  AttributesQueryVariables,
  AttributesValuesQuery,
  AttributesValuesQueryVariables,
  AttributeKind,
  AttributeValueType,
  DocumentsQuery,
  DocumentsQueryVariables,
  DocumentType,
  DocumentQuery,
  DocumentQueryVariables
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import AttributeValueMoney from '~/components/dcis/attributes/fields/AttributeValueMoney.vue'
import AttributeValueNumeric from '~/components/dcis/attributes/fields/AttributeValueNumeric.vue'
import AttributeValueText from '~/components/dcis/attributes/fields/AttributeValueText.vue'
import AttributeValueBigmoney from '~/components/dcis/attributes/fields/AttributeValueBigmoney.vue'
import AttributeValueBool from '~/components/dcis/attributes/fields/AttributeValueBool.vue'
import AttributeValueFiles from '~/components/dcis/attributes/fields/AttributeValueFiles.vue'
import AttributeValueDate from '~/components/dcis/attributes/fields/AttributeValueDate.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import attributesQuery from '~/gql/dcis/queries/attributes.graphql'
import attributesValuesQuery from '~/gql/dcis/queries/attributes_values.graphql'
import { useCommonQuery, useQueryRelay } from '~/composables'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'

type AttributeComponentsType = typeof AttributeValueNumeric | typeof AttributeValueMoney | typeof AttributeValueText

const AttributeValueComponents: Record<AttributeKind, AttributeComponentsType> = {
  TEXT: AttributeValueText,
  MONEY: AttributeValueMoney,
  NUMERIC: AttributeValueNumeric,

  // По умолчанию
  BIGMONEY: AttributeValueBigmoney,
  BOOL: AttributeValueBool,
  FILES: AttributeValueFiles,
  DATE: AttributeValueDate
}

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.documents.links.attributes') as string,
        to: localePath({ name: 'dcis-periods-archive-archiveId-attributes', query: route.query }),
        exact: true
      }
    ]))

    const { data: documents } = useQueryRelay<
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

    const { data: activeDocument } = useCommonQuery<
      DocumentQuery,
      DocumentQueryVariables
    >({
      document: documentQuery,
      variables: () => ({
        documentId: doc.value?.id
      }),
      options: () => ({
        enabled: !!doc.value
      })
    })

    const {
      data: attributes,
      loading: attributesLoading
    } = useCommonQuery<
      AttributesQuery,
      AttributesQueryVariables
    >({
      document: attributesQuery,
      variables: () => ({ periodId: route.params.archiveId })
    })

    const {
      data: attributesValuesData,
      loading: attributesValuesLoading
    } = useCommonQuery<
      AttributesValuesQuery,
      AttributesValuesQueryVariables
    >({
      document: attributesValuesQuery,
      variables: () => ({ documentId: activeDocument.value?.id })
    })

    const loading = computed(() => attributesLoading.value || attributesValuesLoading.value)

    const attributesValues = computed<Record<number, AttributeValueType>>(() => (
      attributesValuesData.value.reduce((a, c) => ({ [c.attributeId]: c, ...a }), {}))
    )

    return {
      AttributeValueComponents,
      bc,
      attributes,
      attributesValues,
      loading
    }
  }
})
</script>
