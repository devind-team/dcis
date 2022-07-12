<template lang="pug">
.grid__selection-view(:style="style")
</template>

<script lang="ts">
import { PropType } from '#app'
import { SelectionViewType } from '~/types/grid'
import { elementPositionToStyle } from '~/services/grid'

export default defineComponent({
  props: {
    selectionView: { type: Object as PropType<SelectionViewType>, required: true }
  },
  setup (props) {
    const style = computed<Record<string, string | number>>(() => ({
      ...elementPositionToStyle(props.selectionView.position),
      width: `${props.selectionView.width}px`,
      height: `${props.selectionView.height}px`,
      ...Object.fromEntries(
        Object.entries(props.selectionView.border)
          .filter(([_, v]) => v).map(([k, _]) => [`border-${k}`, '1px solid blue'])
      )
    }))
    return { style }
  }
})
</script>
