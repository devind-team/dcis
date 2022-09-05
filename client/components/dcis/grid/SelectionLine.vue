<template lang="pug">
  .grid__selection-line(:style="style")
</template>

<script lang="ts">
import { PropType } from '#app'
import { Direction, SelectionLineType } from '~/types/grid'

export default defineComponent({
  props: {
    line: { type: Object as PropType<SelectionLineType>, required: true }
  },
  setup (props) {
    const style = computed<Record<string, string | number>>(() => ({
      left: `${props.line.start.left}px`,
      top: `${props.line.start.top}px`,
      width: props.line.direction === Direction.HORIZONTAL ? `${props.line.length}px` : '1px',
      height: props.line.direction === Direction.VERTICAL ? `${props.line.length}px` : '1px',
      zIndex: props.line.zIndex
    }))

    return { style }
  }
})
</script>
