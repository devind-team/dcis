<template lang="pug">
v-tab-item
  template(v-if="!loading")
    template(v-if="attributes.length")
      component(
        v-for="attribute in attributes"
        :key="attribute.id"
        :is="AttributeValueComponents[attribute.kind]"
        :attribute="attribute"
        :attribute-value="attribute.id in values ? values[attribute.id] : null"
        :readonly="readonly"
        @change="changeValue(attribute, $event)"
      )
    v-alert(v-else type="info") Атрибутов нет
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { useApolloClient, useMutation } from '@vue/apollo-composable'
import {
  AttributeKind,
  AttributeType,
  AttributeValueType,
  ChangeAttributeValueMutation,
  ChangeAttributeValueMutationVariables
} from '~/types/graphql'
import { UpdateActiveSheetType } from '~/types/grid'
import { changeSheetValues } from '~/composables/grid-mutations'
import changeAttributeValueMutation from '~/gql/dcis/mutations/attributes/change_attribute_value.graphql'
import AttributeValueMoney from '~/components/dcis/attributes/fields/AttributeValueMoney.vue'
import AttributeValueNumeric from '~/components/dcis/attributes/fields/AttributeValueNumeric.vue'
import AttributeValueText from '~/components/dcis/attributes/fields/AttributeValueText.vue'
import AttributeValueBigmoney from '~/components/dcis/attributes/fields/AttributeValueBigmoney.vue'
import AttributeValueBool from '~/components/dcis/attributes/fields/AttributeValueBool.vue'
import AttributeValueFiles from '~/components/dcis/attributes/fields/AttributeValueFiles.vue'
import AttributeValueDate from '~/components/dcis/attributes/fields/AttributeValueDate.vue'

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
  components: { AttributeValueText },
  props: {
    documentId: { type: String, required: true },
    loading: { type: Boolean, default: false },
    attributes: { type: Array as PropType<AttributeType[]>, default: () => ([]) },
    attributesValues: { type: Array as PropType<AttributeValueType[]>, default: () => ([]) },
    readonly: { type: Boolean, default: false },
    changeUpdateAttributesValues: {
      type: Function as PropType<(cache, result: ChangeAttributeValueMutationResult, key: string) => void>,
      required: true
    },
    updateActiveSheet: { type: Function as PropType<UpdateActiveSheetType>, required: true }
  },
  setup (props) {
    const { client } = useApolloClient()
    const values = computed<Record<number, AttributeValueType>>(() => (
      props.attributesValues.reduce((a, c) => ({ [c.attributeId]: c, ...a }), {}))
    )
    const { mutate: changeAttributeValue } = useMutation<
      ChangeAttributeValueMutation,
      ChangeAttributeValueMutationVariables
    >(
      changeAttributeValueMutation,
      {
        update: (cache, result: ChangeAttributeValueMutationResult) => {
          if (!result.data.changeAttributeValue.errors.length) {
            props.changeUpdateAttributesValues(cache, result, 'attributeValue')
            const { values } = result.data.changeAttributeValue
            changeSheetValues(values, client, props.documentId)
          }
        }
      }
    )
    const changeValue = (attribute: AttributeType, value: string) => {
      changeAttributeValue({ attributeId: attribute.id, documentId: props.documentId, value: value ?? '' })
    }
    return { AttributeValueComponents, values, changeValue }
  }
})
</script>
