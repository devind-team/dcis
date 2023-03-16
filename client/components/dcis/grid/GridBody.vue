<template lang="pug">
tbody
  tr(
    v-for="row in activeSheet.rows"
    :key="row.id"
    :class="getRowClass(row)"
    :style="getRowStyle(row)"
  )
    td.grid__cell_row-name(
      :class="getRowNameCellClass(row)"
      @mouseenter="mouseenterRowName(row)"
      @mousemove="mousemoveRowName(row, $event)"
      @mouseleave="mouseleaveRowName"
      @mousedown="mousedownRowName(row, $event)"
      @mouseup="mouseupRowName"
    )
      div(:style="getRowNameCellContentStyle(row)" @contextmenu="(e) => showMenu(e, row)") {{ row.name }}
    td(
      v-for="cell in row.cells"
      :key="cell.id"
      :class="getCellClass(cell)"
      :style="getCellStyle(cell)"
      :colspan="cell.colspan"
      :rowspan="cell.rowspan"
      @mousedown="mousedownCell(cell)"
      @mouseenter="mouseenterCell(cell)"
      @dblclick="dblclickCell(cell)"
    )
      grid-cell(
        :style="getCellContentStyle(cell)"
        :cell="cell"
        :active="!!activeCell && activeCell.id === cell.id"
        @clear-active="setActiveCell(null)"
      )
  grid-row-control(
    v-if="!!currentRow"
    :row="currentRow"
    :can-add-before="canAddRowBeforeOrAfter(currentRow)"
    :can-add-after="canAddRowBeforeOrAfter(currentRow)"
    :can-add-inside="canAddRowInside(currentRow)"
    :can-delete="canDeleteRow(currentRow)"
    :get-row-height="getRowHeight"
    :change-row-height="changeRowHeight"
    :reset-row-height="resetRowHeight"
    :clear-selection="clearSelection"
    :pos-x="posX"
    :pos-y="posY"
    @close="currentRow = null"
  )
</template>

<script lang="ts">
import { computed, defineComponent, inject, nextTick, PropType, ref } from '#app'
import { CellType, ColumnDimensionType, RowDimensionType } from '~/types/graphql'
import {
  ActiveSheetInject,
  FixedInfoType,
  GridMode,
  GridModeInject,
  ResizingType,
  RowFixedInfoType
} from '~/types/grid'
import {
  getCellHeightStyle,
  getCellTextFormattingStyle,
  getCellBorderStyle,
  getCellBackgroundStyle,
  getCellExcelStyle
} from '~/services/grid'
import { useCanAddRowBeforeOrAfter, useCanAddRowInside, useCanDeleteRow } from '~/composables/grid-permissions'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    resizingRow: { type: Object as PropType<ResizingType<RowDimensionType>>, default: null },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
    changeRowHeight: {
      type: Function as PropType<(rowDimension: RowDimensionType, height: number) => void>,
      required: true
    },
    resetRowHeight: { type: Function as PropType<(rowDimension: RowDimensionType) => void>, required: true },
    getRowFixedInfo: { type: Function as PropType<(row: RowDimensionType) => RowFixedInfoType>, required: true },
    getCellFixedInfo: { type: Function as PropType<(cell: CellType) => FixedInfoType>, required: true },
    borderFixedColumn: { type: Object as PropType<ColumnDimensionType>, default: null },
    borderFixedRow: { type: Object as PropType<RowDimensionType>, default: null },
    isRowFixedBorder: { type: Function as PropType<(row: RowDimensionType) => boolean>, required: true },
    isCellFixedBorderRight: { type: Function as PropType<(cell: CellType) => boolean>, required: true },
    isCellFixedBorderBottom: { type: Function as PropType<(cell: CellType) => boolean>, required: true },
    selectedCells: { type: Array as PropType<CellType[]>, required: true },
    activeCell: { type: Object as PropType<CellType>, default: null },
    setActiveCell: { type: Function as PropType<(cell: CellType | null) => void>, required: true },
    selectedRowsPositions: { type: Array as PropType<number[]>, required: true },
    boundarySelectedRowsPositions: { type: Array as PropType<number[]>, required: true },
    clearSelection: { type: Function as PropType<() => void>, required: true },
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
    dblclickCell: { type: Function as PropType<(cell: CellType) => void>, required: true }
  },
  setup (props) {
    const mode = inject(GridModeInject)
    const activeSheet = inject(ActiveSheetInject)

    const isFixedSelection = computed<boolean>(() =>
      mode.value === GridMode.READ || mode.value === GridMode.REPORT || mode.value === GridMode.WRITE
    )

    const getRowClass = (row: RowDimensionType): Record<string, boolean> => {
      return {
        grid__row_fixed: isFixedSelection.value && props.getRowFixedInfo(row).fixed
      }
    }
    const getRowStyle = (row: RowDimensionType): Record<string, string> => {
      if (mode.value === GridMode.CHANGE) {
        return {}
      }
      const fixedInfo = props.getRowFixedInfo(row)
      if (fixedInfo.fixed) {
        return {
          top: `${fixedInfo.position}px`,
          zIndex: `${2 + fixedInfo.reverseIndex}`
        }
      }
      return {}
    }

    const canAddRowBeforeOrAfter = useCanAddRowBeforeOrAfter()
    const canAddRowInside = useCanAddRowInside()
    const canDeleteRow = useCanDeleteRow()

    const getRowNameCellClass = (row: RowDimensionType): Record<string, boolean> => {
      return {
        'grid__cell_row-name-selected': props.selectedRowsPositions.includes(row.globalIndex),
        'grid__cell_row-name-boundary-selected': mode.value === GridMode.CHANGE &&
          props.boundarySelectedRowsPositions.includes(row.globalIndex),
        'grid__cell_row-name-hover': mode.value === GridMode.CHANGE && !props.resizingRow,
        'grid__cell_fixed-border-right': isFixedSelection.value && props.borderFixedColumn === null,
        'grid__cell_fixed-border-bottom': isFixedSelection.value && props.isRowFixedBorder(row)
      }
    }
    const getRowNameCellContentStyle = (row: RowDimensionType): Record<string, string> => {
      const style: Record<string, string> = { height: `${props.getRowHeight(row)}px` }
      if (row.background) {
        style.background = row.background
      }
      return style
    }

    const getCellClass = (cell: CellType): Record<string, boolean> => {
      return {
        grid__cell_selected: isFixedSelection.value && Boolean(
          props.selectedCells.find((selectedCell: CellType) => selectedCell.id === cell.id)
        ),
        grid__cell_fixed: isFixedSelection.value && props.getCellFixedInfo(cell).fixed,
        grid__cell_readonly: mode.value !== GridMode.REPORT && !cell.editable,
        'grid__cell_fixed-border-right': isFixedSelection.value && props.isCellFixedBorderRight(cell),
        'grid__cell_fixed-border-bottom': isFixedSelection.value && props.isCellFixedBorderBottom(cell)
      }
    }
    const getCellStyle = (cell: CellType): Record<string, string> => {
      const style: Record<string, string> = {
        ...getCellTextFormattingStyle(cell),
        ...getCellBorderStyle(cell),
        ...getCellExcelStyle(cell)
      }
      if (isFixedSelection.value) {
        const fixedInfo = props.getCellFixedInfo(cell)
        if (fixedInfo.fixed) {
          style.left = `${fixedInfo.position}px`
        }
      }
      return style
    }

    const getCellContentStyle = (cell: CellType): Record<string, string> => {
      const valuesMap = {
        left: 'flex-start',
        top: 'flex-start',
        middle: 'center',
        center: 'center',
        right: 'flex-end',
        bottom: 'flex-end'
      }
      const style: Record<string, string> = {
        ...getCellHeightStyle(cell, props.getRowHeight, activeSheet.value),
        ...getCellBackgroundStyle(cell, activeSheet.value)
      }
      if (cell.horizontalAlign) {
        style['justify-content'] = valuesMap[cell.horizontalAlign]
        style['text-align'] = cell.horizontalAlign
      }
      if (cell.verticalAlign) { style['align-items'] = valuesMap[cell.verticalAlign] }
      return style
    }

    const currentRow = ref<RowDimensionType | null>(null)
    const posX = ref<number>(0)
    const posY = ref<number>(0)
    const showMenu = (e: MouseEvent, row: RowDimensionType) => {
      e.preventDefault()
      currentRow.value = null
      posY.value = e.clientY
      posX.value = e.clientX
      nextTick(() => {
        currentRow.value = row
      })
    }

    return {
      currentRow,
      posX,
      posY,
      showMenu,
      activeSheet,
      getRowClass,
      getRowStyle,
      canAddRowBeforeOrAfter,
      canDeleteRow,
      canAddRowInside,
      getRowNameCellClass,
      getRowNameCellContentStyle,
      getCellClass,
      getCellStyle,
      getCellContentStyle
    }
  }
})
</script>
