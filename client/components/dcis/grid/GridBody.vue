<template lang="pug">
  tbody
    tr(v-for="row in rows" :key="row.id" :style="row.style")
      td.grid__cell_row-index(
        @mouseenter="mouseenterRowIndex(row)"
        @mousedown="mousedownRowIndex(row)"
      )
        grid-row-control(:row="row" :content-class="getRowIndexCellContentClasses(row)")
      td(
        v-for="cell in row.cells"
        :key="cell.id"
        :colspan="cell.colspan"
        :rowspan="cell.rowspan"
        :class="getCellClasses(cell)"
        :style="`${cell.style}`"
        @mousedown="startSelection(cell.position)"
        @mouseenter="enterSelection(cell.position)"
        @mouseup="endSelection(cell.position)"
      )
        grid-cell(
          @clear-active="setActive(null)"
          :cell="cell"
          :active="active === cell.position"
          :selection="selection && selection.includes(cell.position)"
        )
</template>
<script lang="ts">
import { defineComponent, inject } from '#app'
import type { PropType, Ref } from '#app'
import { BuildCellType, BuildRowType, BoundaryColumnCell, RangeType } from '~/types/grid-types'
import GridCell from '~/components/dcis/grid/GridCell.vue'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true },
    selection: { type: Array as PropType<RangeType[]>, default: () => ([]) },
    selectionRows: { type: Array as PropType<number[]>, default: () => ([]) },
    boundaryColumnCells: { type: Array as PropType<BoundaryColumnCell[]>, required: true },
    selectedBoundaryColumnCells: { type: Array as PropType<BoundaryColumnCell[]>, required: true },
    mouseenterRowIndex: { type: Function as PropType<(row: BuildRowType) => void>, required: true },
    mousedownRowIndex: { type: Function as PropType<(row: BuildRowType) => void>, required: true },
    setActive: { type: Function as PropType<(position: string) => void>, required: true },
    startSelection: { type: Function as PropType<(position: string) => void>, required: true },
    enterSelection: { type: Function as PropType<(position: string) => void>, required: true },
    endSelection: { type: Function as PropType<(position: string) => void>, required: true }
  },
  setup (props) {
    const active = inject<Ref<string>>('active')

    const getRowIndexCellContentClasses = (row: BuildRowType): (string | Record<string, boolean>)[] => {
      return [
        'grid__cell-content_row-index',
        { 'grid__cell-content_row-index-selected': props.selectionRows.includes(row.index) },
        {
          'grid__cell-content_row-index-neighbor-selected':
            !!props.selectedBoundaryColumnCells.find(boundaryCell =>
              boundaryCell.rows.find(boundaryColumnCell => boundaryColumnCell.id === row.id))
        }
      ]
    }

    const getCellClasses = (cell: BuildCellType): Record<string, boolean> => ({
      grid__cell_selected: props.selection.includes(cell.position),
      grid__cell_boundary: !!props.boundaryColumnCells.find(boundaryCell => boundaryCell.cell.id === cell.id)
    })

    return { active, getRowIndexCellContentClasses, getCellClasses }
  }
})
</script>
