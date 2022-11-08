<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(v-if="!(attributesLoading || attributesValuesLoading)")
    template(v-if="attributes.length")
      component(
        v-for="attribute in attributes"
        :key="attribute.id"
        :is="AttributeValueComponents[attribute.kind]"
        :attribute="attribute"
        :attribute-value="attribute.id in values ? values[attribute.id] : null"
        :readonly="readonly"
        :change-update-attributes-values="changeUpdateAttributesValues"
        @change="changeValue(attribute, $event)"
      )
    v-alert(v-else type="info") Атрибутов нет
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, ComputedRef, defineComponent, PropType } from '#app'
import { useApolloClient, useMutation } from '@vue/apollo-composable'
import {
  DocumentQuery,
  DocumentQueryVariables,
  AttributesQuery,
  AttributesQueryVariables,
  AttributesValuesQuery,
  AttributesValuesQueryVariables,
  AttributeKind,
  AttributeType,
  AttributeValueType,
  ChangeAttributeValueMutation,
  ChangeAttributeValueMutationVariables
} from '~/types/graphql'
import documentQuery from '~/gql/dcis/queries/document.graphql'
import attributesQuery from '~/gql/dcis/queries/attributes.graphql'
import attributesValuesQuery from '~/gql/dcis/queries/attributes_values.graphql'
import { BreadCrumbsItem } from '~/types/devind'
import changeAttributeValueMutation from '~/gql/dcis/mutations/attributes/change_attribute_value.graphql'
import AttributeValueMoney from '~/components/dcis/attributes/fields/AttributeValueMoney.vue'
import AttributeValueNumeric from '~/components/dcis/attributes/fields/AttributeValueNumeric.vue'
import AttributeValueText from '~/components/dcis/attributes/fields/AttributeValueText.vue'
import AttributeValueBigmoney from '~/components/dcis/attributes/fields/AttributeValueBigmoney.vue'
import AttributeValueBool from '~/components/dcis/attributes/fields/AttributeValueBool.vue'
import AttributeValueFiles from '~/components/dcis/attributes/fields/AttributeValueFiles.vue'
import AttributeValueDate from '~/components/dcis/attributes/fields/AttributeValueDate.vue'
import { changeSheetValues } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

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

export type ChangeAttributeValueMutationResult = { data: Pick<ChangeAttributeValueMutation, 'changeAttributeValue'> }

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> },
    documentId: { type: String, required: true },
    attributes: { type: Array as PropType<AttributeType[]>, default: () => ([]) },
    readonly: { type: Boolean, default: false },
    attributesValues: { type: Array as PropType<AttributeValueType[]>, default: () => ([]) },
    changeUpdateAttributesValues: {
      type: Function as PropType<(cache, result: ChangeAttributeValueMutationResult, key: string) => void>,
      required: true
    }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()
    const { client } = useApolloClient()
    const values = computed<Record<number, AttributeValueType>>(() => (
      props.attributesValues.reduce((a, c) => ({ [c.attributeId]: c, ...a }), {}))
    )
    const { mutate: changeAttributeValue } = useMutation<ChangeAttributeValueMutation, ChangeAttributeValueMutationVariables>(
      changeAttributeValueMutation,
      {
        update: (cache, result: ChangeAttributeValueMutationResult) => {
          if (!result.data.changeAttributeValue.errors.length) {
            props.changeUpdateAttributesValues(cache, result, 'attributeValue')
            const { values } = result.data.changeAttributeValue
            console.log(values)
            changeSheetValues(values, client, props.documentId)
          }
        }
      }
    )
    const changeValue = (attribute: AttributeType, value: string) => {
      changeAttributeValue({ attributeId: attribute.id, documentId: props.documentId, value: value ?? '' })
    }
    const { data: activeDocument, loading: activeDocumentLoading } = useCommonQuery<
      DocumentQuery,
      DocumentQueryVariables
    >({
      document: documentQuery,
      variables: () => ({
        documentId: route.params.documentId
      })
    })

    const { loading: attributesLoading } = useCommonQuery<AttributesQuery, AttributesQueryVariables>({
      document: attributesQuery,
      variables: () => ({ periodId: activeDocument.value?.period.id }),
      options: () => ({ enabled: !activeDocumentLoading.value })
    })

    const { loading: attributesValuesLoading } = useCommonQuery<
      AttributesValuesQuery,
      AttributesValuesQueryVariables
    >({
      document: attributesValuesQuery,
      variables: () => ({ documentId: route.params.documentId }),
      options: () => ({ enabled: !activeDocumentLoading.value })
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.documents.links.attributes') as string,
        to: localePath({ name: 'dcis-documents-documentId-attributes' }),
        exact: true
      }
    ]))

    return {
      bc,
      values,
      activeDocument,
      attributesLoading,
      AttributeValueComponents,
      attributesValuesLoading,
      changeValue
    }
  }
})
</script>
