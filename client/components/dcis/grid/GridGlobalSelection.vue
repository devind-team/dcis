<template lang="pug">
  .grid__global-selection(v-show="globalSelection.visible" :style="style")
</template>

<script lang="ts">
import { PropType } from '#app'
import { GlobalSelectionType } from '~/types/grid'
import { elementPositionToStyle } from '~/services/grid'

export default defineComponent({
  props: {
    globalSelection: { type: Object as PropType<GlobalSelectionType>, required: true },
  },
  setup (props) {
    const style = computed<Record<string, string | number>>(() => ({
      ...elementPositionToStyle(props.globalSelection.position),
      zIndex: props.globalSelection.zIndex,
      width: `${props.globalSelection.width}px`,
      height: `${props.globalSelection.height}px`
    }))
    return { style }
  }
})
</script>
