<template lang="pug">
v-text-field(
  :label="attribute.name"
  :placeholder="attribute.placeholder"
  :key="attribute.key"
  :readonly="!attribute.mutable || readonly"
  :value="attribute.value && attribute.value.value || attribute.default"
  clearable
)
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { AttributeType, AttributeValueType } from '~/types/graphql'

export default defineComponent({
  props: {
    attribute: { type: Object as PropType<AttributeType & { value: AttributeValueType }>, required: true },
    readonly: { type: Boolean, default: false }
  }
})
</script>
