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
      @mouseup="mouseupCell(cell)"
    )
      grid-cell(
        :style="getCellContentStyle(cell)"
        :cell="cell"
        :active="!!activeCell && activeCell.id === cell.id"
        @clear-active="setActiveCell(null)"
      )
  grid-row-control(
    v-if="!!currentRow && viewControl(currentRow)"
    :row="currentRow"
    :can-change-settings="canChangeRowSettings"
    :can-add-before="canAddRowBeforeOrAfter(currentRow)"
    :can-add-after="canAddRowBeforeOrAfter(currentRow)"
    :can-add-inside="canAddRowInside(currentRow)"
    :can-delete="canDeleteRow(currentRow)"
    :get-row-height="getRowHeight"
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
import { positionsToRangeIndices } from '~/services/grid'
import {
  useCanAddRowBeforeOrAfter,
  useCanAddRowInside,
  useCanChangeRowSettings,
  useCanDeleteRow
} from '~/composables/grid-permissions'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    resizingRow: { type: Object as PropType<ResizingType<RowDimensionType>>, default: null },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
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
    mouseupCell: { type: Function as PropType<(cell: CellType) => void>, required: true }
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

    const canChangeRowSettings = useCanChangeRowSettings()
    const canAddRowBeforeOrAfter = useCanAddRowBeforeOrAfter()
    const canAddRowInside = useCanAddRowInside()
    const canDeleteRow = useCanDeleteRow()
    const viewControl = (rowDimension: RowDimensionType): boolean => {
      return canChangeRowSettings.value ||
        canAddRowBeforeOrAfter(rowDimension) ||
        canAddRowInside(rowDimension) ||
        canDeleteRow(rowDimension)
    }

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
      const textDecoration: string[] = []
      const style: Record<string, string> = {}
      if (isFixedSelection.value) {
        const fixedInfo = props.getCellFixedInfo(cell)
        if (fixedInfo.fixed) {
          style.left = `${fixedInfo.position}px`
        }
      }
      if (cell.strong) { style['font-weight'] = 'bold' }
      if (cell.italic) { style['font-style'] = 'italic' }
      if (cell.strike) { textDecoration.push('line-through') }
      if (cell.underline) { textDecoration.push('underline') }
      if (cell.size) { style['font-size'] = `${cell.size}px` }
      if (cell.error) {
        style.color = 'red'
      } else if (cell.color) {
        style.color = cell.color
      }
      if (textDecoration.length) {
        style['text-decoration'] = textDecoration.join(' ')
      }
      const borderColor: Record<string, string | null> = JSON.parse(cell.borderColor)
      for (const position of ['top', 'right', 'bottom', 'left']) {
        if (borderColor[position]) {
          style[`border-${position}`] = `1 px solid ${borderColor[position] || 'black'}`
        }
      }
      if (cell.numberFormat) {
        style['mso-number-format'] = cell.numberFormat
      }
      return style
    }

    const getCellContentStyle = (cell: CellType): Record<string, string> => {
      const row = activeSheet.value.rows.find((row: RowDimensionType) => row.id === cell.rowId)
      const valuesMap = {
        left: 'flex-start',
        top: 'flex-start',
        middle: 'center',
        center: 'center',
        right: 'flex-end',
        bottom: 'flex-end'
      }
      const style: Record<string, string> = {
        height: `${getCellHeight(cell)}px`
      }
      if (cell.horizontalAlign) {
        style['justify-content'] = valuesMap[cell.horizontalAlign]
        style['text-align'] = cell.horizontalAlign
      }
      if (cell.verticalAlign) { style['align-items'] = valuesMap[cell.verticalAlign] }
      if (cell.background && cell.background !== '#FFFFFF') {
        style.background = cell.background
      } else if (row.background) {
        style.background = row.background
      }
      return style
    }

    const getCellHeight = (cell: CellType) => {
      const { minRow, maxRow } = positionsToRangeIndices(cell.relatedGlobalPositions)
      let height = 0
      for (let i = minRow - 1; i <= maxRow - 1; i++) {
        height += props.getRowHeight(activeSheet.value.rows[i])
      }
      return height
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
      canChangeRowSettings,
      canAddRowBeforeOrAfter,
      canDeleteRow,
      canAddRowInside,
      viewControl,
      getRowNameCellClass,
      getRowNameCellContentStyle,
      getCellClass,
      getCellStyle,
      getCellContentStyle
    }
  }
})
</script>
