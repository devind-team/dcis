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
        :readonly="!document.canChangeAttributeValue"
        @change="changeAttributeValue(attribute, $event)"
      )
    v-alert(v-else type="info") {{ $t('dcis.documents.attributes.noAttributes') }}
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { useApolloClient, useMutation } from '@vue/apollo-composable'
import { changeSheetValues } from '~/composables/grid-mutations'
import {
  DocumentType,
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
import changeAttributeValueMutation from '~/gql/dcis/mutations/attributes/change_attribute_value.graphql'

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
    document: { required: true, type: Object as PropType<DocumentType> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()
    const { client } = useApolloClient()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.documents.links.attributes') as string,
        to: localePath({ name: 'dcis-documents-documentId-attributes' }),
        exact: true
      }
    ]))

    const {
      data: attributes,
      loading: attributesLoading
    } = useCommonQuery<
      AttributesQuery,
      AttributesQueryVariables
    >({
      document: attributesQuery,
      variables: () => ({ periodId: props.document.period.id })
    })

    const {
      data: attributesValuesData,
      loading: attributesValuesLoading,
      changeUpdate: changeAttributesValuesUpdate
    } = useCommonQuery<
      AttributesValuesQuery,
      AttributesValuesQueryVariables
    >({
      document: attributesValuesQuery,
      variables: () => ({ documentId: route.params.documentId })
    })

    const loading = computed(() => attributesLoading.value || attributesValuesLoading.value)

    const attributesValues = computed<Record<number, AttributeValueType>>(() => (
      attributesValuesData.value.reduce((a, c) => ({ [c.attributeId]: c, ...a }), {}))
    )

    const { mutate: changeAttributeValueMutate } = useMutation<
      ChangeAttributeValueMutation,
      ChangeAttributeValueMutationVariables
    >(
      changeAttributeValueMutation,
      {
        update: (cache, result: ChangeAttributeValueMutationResult) => {
          if (!result.data.changeAttributeValue.errors.length) {
            changeAttributesValuesUpdate(cache, result, 'attributeValue')
            const { values } = result.data.changeAttributeValue
            changeSheetValues(values, client, props.document.id)
          }
        }
      }
    )
    const changeAttributeValue = (attribute: AttributeType, value: string) => {
      changeAttributeValueMutate({
        attributeId: attribute.id,
        documentId: props.document.id,
        value: value ?? ''
      })
    }

    return {
      AttributeValueComponents,
      bc,
      attributes,
      attributesValues,
      loading,
      changeAttributeValue
    }
  }
})
</script>
