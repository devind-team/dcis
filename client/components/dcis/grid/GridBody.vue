<template lang="pug">
  tbody
    tr(v-for="buildRow in rows" :key="buildRow.rowDimension.id")
      td.grid__cell_row-name(
        :class="{ 'grid__cell_row-name-hover': !resizingRow }"
        @mouseenter="mouseenterRowName(buildRow)"
        @mousemove="mousemoveRowName(buildRow, $event)"
        @mouseleave="mouseleaveRowName"
        @mousedown="mousedownRowName(buildRow, $event)"
        @mouseup="mouseupRowName"
      )
        grid-row-control(v-slot="{ onMenu, onTooltip, attrs }" :build-row="buildRow" :get-row-height="getRowHeight")
          .grid__cell-content_row-name(
            v-bind="attrs"
            v-on="onTooltip"
            @contextmenu.prevent="onMenu.click"
            :class="getRowNameCellContentClasses(buildRow)"
            :style="{ height: `${getRowHeight(buildRow) + 1}px` }"
          ) {{ buildRow.rowDimension.name }}
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
          :style="{ height: `${getRowHeight(buildRow)}px` }"
          :build-cell="buildCell"
          :active="activeCell && activeCell.cell.id === buildCell.cell.id"
          @clear-active="setActiveCell(null)"
        )
</template>

<script lang="ts">
import { PropType } from '#app'
import { ResizingType, BuildRowType, BuildCellType, BoundaryColumnCell } from '~/types/grid'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true },
    resizingRow: { type: Object as PropType<ResizingType<BuildRowType>>, default: null },
    getRowHeight: { type: Function as PropType<(buildRow: BuildRowType) => number>, required: true },
    activeCell: { type: Object as PropType<BuildCellType>, default: null },
    setActiveCell: { type: Function as PropType<(buildCell: BuildCellType | null) => void>, required: true },
    selectedCellsPositions: { type: Array as PropType<string[]>, required: true },
    selectedRowsPositions: { type: Array as PropType<number[]>, required: true },
    boundaryColumnCells: { type: Array as PropType<BoundaryColumnCell[]>, required: true },
    selectedBoundaryColumnCells: { type: Array as PropType<BoundaryColumnCell[]>, required: true },
    mouseenterRowName: {
      type: Function as PropType<(buildRow: BuildRowType) => void>,
      required: true
    },
    mousemoveRowName: {
      type: Function as PropType<(buildRow: BuildRowType, event: MouseEvent) => void>,
      required: true
    },
    mouseleaveRowName: { type: Function as PropType<() => void>, required: true },
    mousedownRowName: {
      type: Function as PropType<(buildRow: BuildRowType, event: MouseEvent) => void>,
      required: true
    },
    mouseupRowName: { type: Function as PropType<() => void>, required: true },
    mousedownCell: { type: Function as PropType<(buildCell: BuildCellType) => void>, required: true },
    mouseenterCell: { type: Function as PropType<(buildCell: BuildCellType) => void>, required: true },
    mouseupCell: { type: Function as PropType<(buildCell: BuildCellType) => void>, required: true }
  },
  setup (props) {
    const getRowNameCellContentClasses = (buildRow: BuildRowType): Record<string, boolean> => {
      return {
        'grid__cell-content_row-name-selected': props.selectedRowsPositions
          .includes(buildRow.rowDimension.globalIndex),
        'grid__cell-content_row-name-neighbor-selected': !!props.selectedBoundaryColumnCells.find(boundaryCell =>
          boundaryCell.buildRows.find(boundaryColumnRow =>
            boundaryColumnRow.rowDimension.id === buildRow.rowDimension.id))
      }
    }

    const getCellClasses = (buildCell: BuildCellType): Record<string, boolean> => ({
      grid__cell_selected: props.selectedCellsPositions.includes(buildCell.cell.globalPosition),
      grid__cell_boundary: !!props.boundaryColumnCells.find(
        boundaryCell => boundaryCell.buildCell.cell.id === buildCell.cell.id
      )
    })

    return { getRowNameCellContentClasses, getCellClasses }
  }
})
</script>
