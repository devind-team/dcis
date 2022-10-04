<template lang="pug">
v-tab-item
  template(v-if="!attributesLoading")
    component(
      v-for="attribute in attributes"
      :key="attribute.id"
      :is="AttributeValueComponents[attribute.kind]"
      :attribute="attribute"
      :readonly="readonly"
    )
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { AttributeKind, AttributeType, AttributeValueType } from '~/types/graphql'

import AttributeValueMoney from '~/components/dcis/attributes/fields/AttributeValueMoney.vue'
import AttributeValueNumeric from '~/components/dcis/attributes/fields/AttributeValueNumeric.vue'
import AttributeValueText from '~/components/dcis/attributes/fields/AttributeValueText.vue'

type AttributeComponentsType = typeof AttributeValueNumeric | typeof AttributeValueMoney | typeof AttributeValueText

const AttributeValueComponents: Record<AttributeKind, AttributeComponentsType> = {
  TEXT: AttributeValueText,
  MONEY: AttributeValueMoney,
  NUMERIC: AttributeValueNumeric,

  // По умолчанию
  BIGMONEY: AttributeValueText,
  BOOL: AttributeValueText,
  FILES: AttributeValueText,
  DATE: AttributeValueText
}

export default defineComponent({
  props: {
    attributesLoading: { type: Boolean, default: false },
    attributes: { type: Array as PropType<(AttributeType & { value: AttributeValueType })[]>, default: () => ([]) },
    readonly: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    return { AttributeValueComponents }
  }
})
</script>
