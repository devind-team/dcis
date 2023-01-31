<template lang="pug">
v-alert.grid__element-resizing.font-weight-medium.px-1.py-0(
  v-show="elementResizing.visible"
  :class="isDark ? 'grid__element-resizing_dark' : 'grid__element-resizing_light'"
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
import { useVuetify } from '~/composables'

export default defineComponent({
  props: {
    message: { type: String, required: true },
    elementResizing: { type: Object as PropType<ElementResizingType>, required: true }
  },
  setup (props) {
    const { isDark } = useVuetify()

    const style = computed<Record<string, string>>(() => elementPositionToStyle(props.elementResizing.position))
    return { style, isDark }
  }
})
</script>
