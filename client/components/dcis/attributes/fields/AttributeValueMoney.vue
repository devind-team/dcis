<template lang="pug">
v-text-field(
  v-model="value"
  @keyup.enter="$event.target.blur()"
  @blur="change"
  :label="attribute.name"
  :placeholder="attribute.placeholder"
  :key="attribute.key"
  :readonly="!attribute.mutable || readonly"
  :clearable="!readonly"
)
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch } from '#app'
import { AttributeType, AttributeValueType } from '~/types/graphql'
import { useFilters } from '~/composables'

export default defineComponent({
  props: {
    attribute: { type: Object as PropType<AttributeType>, required: true },
    attributeValue: { type: Object as PropType<AttributeValueType>, default: null },
    readonly: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const { money } = useFilters()
    const value = ref<string>(money(props.attributeValue?.value || props.attribute.default))
    watch(() => props.attributeValue, () => {
      value.value = money(props.attributeValue?.value || props.attribute.default)
    })
    const change = () => {
      if (props.attribute.mutable && !props.readonly) {
        emit('change', value.value)
      }
    }
    return { value, change }
  }
})
</script>
