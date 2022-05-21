<template lang="pug">
  .grid__cell-content(:class="contentClasses")
    component(
      v-if="active && cell.editable"
      :is="`GridCell${cellKind}`"
      :value="cell.value"
      @cancel="$emit('clear-active')"
    )
    template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { CellType } from '~/types/graphql'
import { cellKinds } from '~/composables/grid'
import GridCellNumeric from '~/components/dcis/grid/cells/GridCellNumeric.vue'
import GridCellString from '~/components/dcis/grid/cells/GridCellString.vue'
import GridCellText from '~/components/dcis/grid/cells/GridCellText.vue'
import GridCellMoney from '~/components/dcis/grid/cells/GridCellMoney.vue'
import GridCellDepartment from '~/components/dcis/grid/cells/GridCellDepartment.vue'
import GridCellUser from '~/components/dcis/grid/cells/GridCellUser.vue'
import GridCellClassification from '~/components/dcis/grid/cells/GridCellClassification.vue'

export default defineComponent({
  components: {
    GridCellNumeric,
    GridCellString,
    GridCellText,
    GridCellMoney,
    GridCellDepartment,
    GridCellUser,
    GridCellClassification
  },
  props: {
    cell: { type: Object as PropType<CellType>, required: true },
    active: { type: Boolean, default: false }
  },
  setup (props) {
    const cellKind = computed<string>(() => (
      props.cell.kind in cellKinds ? cellKinds[props.cell.kind] : 'String'
    ))

    const contentClasses = computed<Record<string, boolean>>(() => ({
      'grid__cell-content_active': props.active && ['n', 's', 'money'].includes(props.cell.kind)
    }))

    return { cellKind, contentClasses }
  }
})
</script>
