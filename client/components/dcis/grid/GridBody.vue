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
      div(:style="{ height: `${getRowHeight(row)}px` }" @contextmenu="(e) => showMenu(e, row)") {{ row.name }}
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
        :style="getCellContentStyle(row, cell)"
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
import { PropType, Ref, nextTick } from '#app'
import { CellType, RowDimensionType, SheetType } from '~/types/graphql'
import { GridMode, ResizingType } from '~/types/grid'
import { useAuthStore } from '~/stores'
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
    const userStore = useAuthStore()

    const mode = inject<GridMode>('mode')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')

    const rootCount = computed<number>(() => activeSheet.value.rows
      .reduce((a: number, c: RowDimensionType) => c.parent ? a : a + 1, 0))

    const getRowNameCellClass = (row: RowDimensionType): Record<string, boolean> => {
      return {
        'grid__cell_row-name-selected': props.selectedRowsPositions.includes(row.globalIndex),
        'grid__cell_row-name_boundary-selected': props.boundarySelectedRowsPositions.includes(row.globalIndex),
        'grid__cell_row-name-hover': !props.resizingRow
      }
    }

    const canChangeRowSettings = mode === GridMode.CHANGE
    const canAddRowBeforeOrAfter = (rowDimension: RowDimensionType): boolean => {
      if (mode === GridMode.CHANGE) {
        return true
      }
      if (rowDimension.parent) {
        const parent = activeSheet.value.rows.find((row: RowDimensionType) => rowDimension.parent.id === row.id)
        return parent.dynamic && activeSheet.value.canChange
      }
      return false
    }
    const canAddRowInside = (rowDimension: RowDimensionType): boolean => {
      if (mode === GridMode.CHANGE) {
        return false
      }
      return rowDimension.dynamic && activeSheet.value.canChange
    }
    const canDeleteRow = (rowDimension: RowDimensionType): boolean => {
      if (mode === GridMode.CHANGE) {
        return rootCount.value !== 1 || Boolean(rowDimension.parent)
      } else {
        return rowDimension.parent !== null && rowDimension.children.length === 0 && (
          activeSheet.value.canChange || rowDimension.userId === userStore.user.id
        )
      }
    }
    const viewControl = (rowDimension: RowDimensionType): boolean => {
      return canChangeRowSettings ||
        canAddRowBeforeOrAfter(rowDimension) ||
        canAddRowInside(rowDimension) ||
        canDeleteRow(rowDimension)
    }

    const getCellStyle = (cell: CellType): Record<string, string> => {
      const textDecoration: string[] = []
      const style: Record<string, string> = {}
      if (cell.strong) { style['font-weight'] = 'bold' }
      if (cell.italic) { style['font-style'] = 'italic' }
      if (cell.strike) { textDecoration.push('line-through') }
      if (cell.underline) { textDecoration.push('underline') }
      if (cell.size) { style['font-size'] = `${cell.size}px` }
      if (cell.color) { style['font-color'] = cell.color }
      if (cell.background) { style['background-color'] = cell.background }
      style['text-decoration'] = textDecoration.join(' ')
      const borderColor: Record<string, string | null> = JSON.parse(cell.borderColor)
      for (const position of ['top', 'right', 'bottom', 'left']) {
        if (borderColor[position]) {
          cell[`border-${position}`] = `1 px solid ${borderColor[position] || 'black'}`
        }
      }
      return style
    }

    const getCellContentStyle = (row: RowDimensionType, cell: CellType): Record<string, string> => {
      const valuesMap = {
        left: 'flex-start',
        top: 'flex-start',
        middle: 'center',
        center: 'center',
        right: 'flex-end',
        bottom: 'flex-end'
      }
      const style: Record<string, string> = {
        height: cell.rowspan === 1 ? `${props.getRowHeight(row)}px` : '100%'
      }
      if (cell.horizontalAlign) {
        style['justify-content'] = valuesMap[cell.horizontalAlign]
        style['text-align'] = cell.horizontalAlign
      }
      if (cell.verticalAlign) { style['align-items'] = valuesMap[cell.verticalAlign] }
      return style
    }
    const currentRow = ref<RowDimensionType>(null)
    const posX = ref(0)
    const posY = ref(0)
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
      getRowNameCellClass,
      canChangeRowSettings,
      canAddRowBeforeOrAfter,
      canDeleteRow,
      canAddRowInside,
      viewControl,
      getCellStyle,
      getCellContentStyle
    }
  }
})
</script>
