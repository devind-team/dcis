<template lang="pug">
  .grid__cell-content(:class="contentClasses")
    component(
      v-if="active && cell.editable"
      :is="`GridCell${cellKind}`"
      :value="cell.value"
      @set-value="setValue"
      @cancel="$emit('clear-active')"
    )
    template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { PropType, Ref } from '#app'
import { UpdateType } from '~/composables'
import { DocumentType, SheetQuery, SheetType, CellType } from '~/types/graphql'
import { cellKinds } from '~/composables/grid'
import GridCellNumeric from '~/components/dcis/grid/cells/GridCellNumeric.vue'
import GridCellString from '~/components/dcis/grid/cells/GridCellString.vue'
import GridCellText from '~/components/dcis/grid/cells/GridCellText.vue'
import GridCellMoney from '~/components/dcis/grid/cells/GridCellMoney.vue'
import GridCellDepartment from '~/components/dcis/grid/cells/GridCellDepartment.vue'
import GridCellClassification from '~/components/dcis/grid/cells/GridCellClassification.vue'

export default defineComponent({
  components: {
    GridCellNumeric,
    GridCellString,
    GridCellText,
    GridCellMoney,
    GridCellDepartment,
    GridCellClassification
  },
  props: {
    cell: { type: Object as PropType<CellType>, required: true },
    active: { type: Boolean, default: false }
  },
  setup (props) {
    const activeDocument = inject<Ref<DocumentType>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateType<SheetQuery>>>('updateActiveSheet')

    const changeValue = useChangeValueMutation(
      toRef(activeSheet.value, 'id'),
      toRef(activeDocument.value, 'id'),
      updateSheet
    )

    const setValue = async (value: string) => {
      if (props.cell.kind === 'fl') {
        console.log('File')
      } else if (props.cell.value !== value) {
        await changeValue(props.cell, value)
      }
    }

    const cellKind = computed<string>(() => (
      props.cell.kind in cellKinds ? cellKinds[props.cell.kind] : 'String'
    ))

    const contentClasses = computed<Record<string, boolean>>(() => ({
      'grid__cell-content_active': props.active && ['n', 's', 'money'].includes(props.cell.kind)
    }))

    return { setValue, cellKind, contentClasses }
  }
})
</script>
