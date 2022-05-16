<template lang="pug">
  tbody
    tr(v-for="buildRow in rows" :key="buildRow.rowDimension.id" :style="buildRow.style")
      td.grid__cell_row-index(
        @mouseenter="mouseenterRowIndex(buildRow)"
        @mousedown="mousedownRowIndex(buildRow)"
      )
        grid-row-control(:build-row="buildRow" :content-class="getRowIndexCellContentClasses(buildRow)")
      td(
        v-for="buildCell in buildRow.buildCells"
        :key="buildCell.cell.id"
        :colspan="buildCell.cell.colspan"
        :rowspan="buildCell.cell.rowspan"
        :class="getCellClasses(buildCell)"
        :style="buildCell.style"
        @mousedown="mousedownCell(buildCell)"
        @mouseenter="mouseenterCell(buildCell)"
        @mouseup="mouseupCell(buildCell)"
      )
        grid-cell(
          :build-cell="buildCell"
          :active="activeCell && activeCell.cell.id === buildCell.cell.id"
          @clear-active="setActiveCell(null)"
        )
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildRowType, BuildCellType, BoundaryColumnCell } from '~/types/grid'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true },
    activeCell: { type: Object as PropType<BuildCellType>, default: null },
    setActiveCell: { type: Function as PropType<(buildCell: BuildCellType | null) => void>, required: true },
    selectedCellsPositions: { type: Array as PropType<string[]>, required: true },
    selectedRowsPositions: { type: Array as PropType<number[]>, required: true },
    boundaryColumnCells: { type: Array as PropType<BoundaryColumnCell[]>, required: true },
    selectedBoundaryColumnCells: { type: Array as PropType<BoundaryColumnCell[]>, required: true },
    mouseenterRowIndex: { type: Function as PropType<(buildRow: BuildRowType) => void>, required: true },
    mousedownRowIndex: { type: Function as PropType<(buildRow: BuildRowType) => void>, required: true },
    mousedownCell: { type: Function as PropType<(buildCell: BuildCellType) => void>, required: true },
    mouseenterCell: { type: Function as PropType<(buildCell: BuildCellType) => void>, required: true },
    mouseupCell: { type: Function as PropType<(buildCell: BuildCellType) => void>, required: true }
  },
  setup (props) {
    const getRowIndexCellContentClasses = (buildRow: BuildRowType): (string | Record<string, boolean>)[] => {
      return [
        'grid__cell-content_row-index',
        {
          'grid__cell-content_row-index-selected': props.selectedRowsPositions
            .includes(buildRow.rowDimension.globalIndex)
        },
        {
          'grid__cell-content_row-index-neighbor-selected': !!props.selectedBoundaryColumnCells.find(boundaryCell =>
            boundaryCell.buildRows.find(boundaryColumnRow =>
              boundaryColumnRow.rowDimension.id === buildRow.rowDimension.id))
        }
      ]
    }

    const getCellClasses = (buildCell: BuildCellType): Record<string, boolean> => ({
      grid__cell_selected: props.selectedCellsPositions.includes(buildCell.cell.globalPosition),
      grid__cell_boundary: !!props.boundaryColumnCells.find(
        boundaryCell => boundaryCell.buildCell.cell.id === buildCell.cell.id
      )
    })

    return { getRowIndexCellContentClasses, getCellClasses }
  }
})
</script>
