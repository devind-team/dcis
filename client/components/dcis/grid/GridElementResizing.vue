<template lang="pug">
  v-alert.grid__element-resizing.font-weight-medium.px-1.py-0(
    v-show="visible",
    :style="style"
    dense
    outlined
  ) {{ message }}
    span.primary--text {{ size }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import type { ElementPositionType } from '~/types/grid'

export default defineComponent({
  props: {
    message: { type: String, required: true },
    visible: { type: Boolean, required: true },
    position: { type: Object as PropType<ElementPositionType>, required: true },
    size: { type: Number, required: true }
  },
  setup (props) {
    const style = computed<Record<string, string>>(() =>
      Object.entries(props.position)
        .filter(([_, v]) => v !== null)
        .reduce((acc, [k, v]) => ({ ...acc, [k]: `${v}px` }), {})
    )
    return { style }
  }
})
</script>
