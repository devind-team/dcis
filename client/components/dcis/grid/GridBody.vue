<template lang="pug">
  tbody
    tr(v-for="row in activeSheet.rows" :key="row.id")
      td.grid__cell_row-name(
        :class="getRowNameCellClass(row)"
        @mouseenter="mouseenterRowName(row)"
        @mousemove="mousemoveRowName(row, $event)"
        @mouseleave="mouseleaveRowName"
        @mousedown="mousedownRowName(row, $event)"
        @mouseup="mouseupRowName"
      )
        grid-row-control(v-slot="{ onMenu, onTooltip, attrs }" :row="row" :get-row-height="getRowHeight")
          div(
            :style="{ height: `${getRowHeight(row)}px` }"
            @contextmenu.prevent="onMenu.click"
          ) {{ row.name }}
      td(
        v-for="cell in row.cells"
        :key="cell.id"
        :colspan="cell.colspan"
        :rowspan="cell.rowspan"
        :style="getCellStyle(cell)"
        @mousedown="mousedownCell(cell)"
        @mouseenter="mouseenterCell(cell)"
        @mouseup="mouseupCell(cell)"
      )
        grid-cell(
          :style="{ height: `${getRowHeight(row)}px` }"
          :cell="cell"
          :active="activeCell && activeCell.id === cell.id"
          @clear-active="setActiveCell(null)"
        )
</template>

<script lang="ts">
import { PropType, Ref } from '#app'
import { SheetType, RowDimensionType, CellType } from '~/types/graphql'
import { ResizingType } from '~/types/grid'
import { getCellStyle } from '~/services/grid'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    resizingRow: { type: Object as PropType<ResizingType<RowDimensionType>>, default: null },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
    activeCell: { type: Object as PropType<CellType>, default: null },
    setActiveCell: { type: Function as PropType<(cell: CellType | null) => void>, required: true },
    selectedRowsPositions: { type: Array as PropType<number[]>, required: true },
    boundarySelectedRowsPositions: { type: Array as PropType<number[]>, required: true },
    mouseenterRowName: {
      type: Function as PropType<(row: RowDimensionType) => void>,
      required: true
    },
    mousemoveRowName: {
      type: Function as PropType<(row: RowDimensionType, event: MouseEvent) => void>,
      required: true
    },
    mouseleaveRowName: { type: Function as PropType<() => void>, required: true },
    mousedownRowName: {
      type: Function as PropType<(row: RowDimensionType, event: MouseEvent) => void>,
      required: true
    },
    mouseupRowName: { type: Function as PropType<() => void>, required: true },
    mousedownCell: { type: Function as PropType<(cell: CellType) => void>, required: true },
    mouseenterCell: { type: Function as PropType<(cell: CellType) => void>, required: true },
    mouseupCell: { type: Function as PropType<(cell: CellType) => void>, required: true }
  },
  setup (props) {
    const activeSheet = inject<Ref<SheetType>>('activeSheet')

    const getRowNameCellClass = (row: RowDimensionType): Record<string, boolean> => {
      return {
        'grid__cell_row-name-selected': props.selectedRowsPositions.includes(row.globalIndex),
        'grid__cell_row-name_boundary-selected': props.boundarySelectedRowsPositions.includes(row.globalIndex),
        'grid__cell_row-name-hover': !props.resizingRow
      }
    }

    return { activeSheet, getRowNameCellClass, getCellStyle }
  }
})
</script>
