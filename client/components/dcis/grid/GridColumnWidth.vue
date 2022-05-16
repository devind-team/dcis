<template lang="pug">
  v-alert.grid__column-width.font-weight-medium.px-1.py-0(
    v-show="visible",
    :style="style"
    dense
    outlined
  ) {{ t('dcis.grid.columnWidth.width') }}
    span.primary--text {{ width }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import type { ElementPositionType } from '~/types/grid'

export default defineComponent({
  props: {
    visible: { type: Boolean, required: true },
    position: { type: Object as PropType<ElementPositionType>, required: true },
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
