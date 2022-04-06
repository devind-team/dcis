<template lang="pug">
  v-alert.grid-column-width.font-weight-medium.px-1.py-0(
    v-show="visible",
    :style="{ left: `${position.x}px`, top: `${position.y}px` }"
    dense
    outlined
  )
    = 'Ширина: '
    span.primary--text {{ width }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { PositionType } from '~/types/grid-types'

export default defineComponent({
  props: {
    visible: { type: Boolean, required: true },
    position: { type: Object as PropType<PositionType>, required: true },
    width: { type: Number, required: true }
  }
})
</script>

<style lang="sass">
  .grid-column-width
    position: absolute
    z-index: 2
    font-size: 12px
    background: white !important
</style>
