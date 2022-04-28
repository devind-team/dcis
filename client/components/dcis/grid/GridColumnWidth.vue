<template lang="pug">
  v-alert.grid-column-width.font-weight-medium.px-1.py-0(
    v-show="visible",
    :style="style"
    dense
    outlined
  ) {{ t('dcis.grid.columnWidth.width') }}
    span.primary--text {{ width }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import type { PositionType } from '~/types/grid-types'

export default defineComponent({
  props: {
    visible: { type: Boolean, required: true },
    position: { type: Object as PropType<PositionType>, required: true },
    width: { type: Number, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const style = computed<Record<string, string>>(() =>
      Object.entries(props.position)
        .filter(([_, v]) => v !== null)
        .reduce((acc, [k, v]) => ({ ...acc, [k]: `${v}px` }), {})
    )
    return { t, style }
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
