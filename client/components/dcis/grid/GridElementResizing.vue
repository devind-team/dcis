<template lang="pug">
v-alert.grid__element-resizing.font-weight-medium.px-1.py-0(
  v-show="elementResizing.visible"
  :style="style"
  dense
  outlined
) {{ message }}
  span.primary--text {{ elementResizing.size }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { ElementResizingType } from '~/types/grid'
import { elementPositionToStyle } from '~/services/grid'

export default defineComponent({
  props: {
    message: { type: String, required: true },
    elementResizing: { type: Object as PropType<ElementResizingType>, required: true },
  },
  setup (props) {
    const style = computed<Record<string, string>>(() => elementPositionToStyle(props.elementResizing.position))
    return { style }
  }
})
</script>
