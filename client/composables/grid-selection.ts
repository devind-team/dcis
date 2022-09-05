import { useEventListener } from '@vueuse/core'
import { Ref } from '#app'
import { CellType, ColumnDimensionType, RowDimensionType, SheetType } from '~/types/graphql'
import {
  CellsOptionsType,
  ColumnDimensionsOptionsType,
  Direction,
  RangeIndicesType,
  RowDimensionsOptionsType,
  ScrollInfoType,
  SelectionLineType,
  SelectionType
} from '~/types/grid'
import {
  filterCells,
  findCell,
  getCellOptions,
  getColumnDimensionsOptions,
  getRelatedGlobalPositions,
  getRowDimensionsOptions,
  parsePosition,
  positionsToRangeIndices,
  rangeIndicesToPositions
} from '~/services/grid'

export function useGridSelection (
  sheet: Ref<SheetType>,
  scroll: Ref<ScrollInfoType>,
  grid: Ref<HTMLTableElement | null>,
  setActiveCell: (cell: CellType | null) => void
) {
  const selectionState = ref<'cell' | 'column' | 'row' | null>(null)

  const cellsSelection = ref<SelectionType<CellType> | null>(null)
  const columnsSelection = ref<SelectionType<ColumnDimensionType> | null>(null)
  const rowsSelection = ref<SelectionType<RowDimensionType> | null>(null)

  const selectedCells = computed<CellType[]>(() => {
    if (!cellsSelection.value) {
      return []
    }
    let selectedCells = [cellsSelection.value.first, cellsSelection.value.last]
    let newSelectedCells: CellType[] = []
    while (selectedCells.length !== newSelectedCells.length) {
      if (newSelectedCells.length) {
        selectedCells = newSelectedCells
        newSelectedCells = []
      }
      const relatedPositions = getRelatedGlobalPositions(selectedCells)
      const selectedPositions = rangeIndicesToPositions(positionsToRangeIndices(relatedPositions))
      for (const position of selectedPositions) {
        const cell = findCell(sheet.value, (c: CellType) => c.relatedGlobalPositions.includes(position))
        if (cell && !newSelectedCells.find((c: CellType) => c.id === cell.id)) {
          newSelectedCells.push(cell)
        }
      }
    }
    return newSelectedCells
  })
  const selectedColumns = computed<ColumnDimensionType[]>(() => {
    if (!columnsSelection.value) {
      return []
    }
    const indices = [columnsSelection.value.last.index, columnsSelection.value.first.index]
    const minIndex = Math.min(...indices)
    const maxIndex = Math.max(...indices)
    return sheet.value.columns.slice(minIndex - 1, maxIndex)
  })
  const selectedRows = computed<RowDimensionType[]>(() => {
    if (!rowsSelection.value) {
      return []
    }
    const indices = [rowsSelection.value.last.globalIndex, rowsSelection.value.first.globalIndex]
    const minIndex = Math.min(...indices)
    const maxIndex = Math.max(...indices)
    return sheet.value.rows.slice(minIndex - 1, maxIndex)
  })

  const selectedColumnsCells = computed<CellType[]>(() => selectedColumns.value
    .reduce((acc: CellType[], column: ColumnDimensionType) => {
      acc.push(...filterCells(sheet.value, (c: CellType) => {
        const parsedPosition = parsePosition(c.globalPosition)
        return parsedPosition.column === column.name
      }))
      return acc
    }, []))
  const selectedRowsCells = computed<CellType[]>(() => selectedRows.value
    .reduce((acc: CellType[], row: RowDimensionType) => {
      acc.push(...row.cells)
      return acc
    }, []))

  const selectedCellsPositions = computed<string[]>(() => getRelatedGlobalPositions(selectedCells.value))
  const selectedRangeIndices = computed<RangeIndicesType | null>(() => {
    if (selectedCellsPositions.value.length) {
      return positionsToRangeIndices(selectedCellsPositions.value)
    }
    return null
  })
  const allCellsSelected = computed<boolean>(() => {
    return selectedRangeIndices.value !== null &&
      selectedRangeIndices.value.minColumn === 1 &&
      selectedRangeIndices.value.minRow === 1 &&
      selectedRangeIndices.value.maxColumn === sheet.value.columns.at(-1).index &&
      selectedRangeIndices.value.maxRow === sheet.value.rows.at(-1).globalIndex
  })

  const selectedColumnsPositions = computed<number[]>(() => {
    if (selectedColumns.value.length) {
      return selectedColumns.value.map((column: ColumnDimensionType) => column.index)
    }
    if (selectedRangeIndices.value) {
      return Array.from({
        length: selectedRangeIndices.value.maxColumn - selectedRangeIndices.value.minColumn + 1
      }).map((_, i) => i + selectedRangeIndices.value.minColumn)
    }
    return []
  })
  const selectedRowsPositions = computed<number[]>(() => {
    if (selectedRows.value.length) {
      return selectedRows.value.map((row: RowDimensionType) => row.globalIndex)
    }
    if (selectedRangeIndices.value) {
      return Array.from({
        length: selectedRangeIndices.value.maxRow - selectedRangeIndices.value.minRow + 1
      }).map((_, i) => i + selectedRangeIndices.value.minRow)
    }
    return []
  })

  const theadRow = ref<HTMLTableRowElement | null>(null)
  onMounted(() => {
    theadRow.value = grid.value.querySelector('thead tr') as HTMLTableRowElement
  })

  const selectionLines = computed<SelectionLineType[]>(() => {
    if (columnsSelection.value) {
      const indices = [columnsSelection.value.first.index, columnsSelection.value.last.index]
      const firstColumnIndex = Math.min(...indices)
      const firstColumn = theadRow.value.cells.item(firstColumnIndex) as HTMLTableCellElement
      const lastColumn = theadRow.value.cells.item(Math.max(...indices)) as HTMLTableCellElement
      const left = firstColumn.offsetLeft - 1
      const top = scroll.value.top + firstColumn.offsetHeight - 1
      const width = lastColumn.offsetLeft + lastColumn.offsetWidth - firstColumn.offsetLeft
      const height = grid.value.offsetHeight - theadRow.value.offsetHeight - scroll.value.top
      const lines = [
        { start: { left, top }, length: height, direction: Direction.VERTICAL, zIndex: 3 },
        { start: { left: left + width, top }, length: height, direction: Direction.VERTICAL, zIndex: 3 }
      ]
      if (scroll.value.top === 0) {
        lines.push({ start: { left, top }, length: width, direction: Direction.HORIZONTAL, zIndex: 3 })
      }
      if (scroll.value.top === scroll.value.height) {
        lines.push({ start: { left, top: top + height }, length: width, direction: Direction.HORIZONTAL, zIndex: 3 })
      }
      return lines
    }
    return []
  })

  const selectedCellsOptions = computed<CellsOptionsType | null>(() => {
    if (cellsSelection.value) {
      return getCellOptions(selectedCells.value)
    }
    if (columnsSelection.value) {
      return getCellOptions(selectedColumnsCells.value)
    }
    if (rowsSelection.value) {
      return getCellOptions(selectedRowsCells.value)
    }
    return null
  })
  const selectedColumnDimensionsOptions = computed<ColumnDimensionsOptionsType | null>(() => {
    if (columnsSelection.value) {
      return getColumnDimensionsOptions(selectedColumns.value, selectedColumnsCells.value, sheet.value.rows.length)
    }
    return null
  })
  const selectedRowDimensionsOptions = computed<RowDimensionsOptionsType | null>(() => {
    if (rowsSelection.value) {
      return getRowDimensionsOptions(selectedRows.value, selectedRowsCells.value, sheet.value.columns.length)
    }
    return null
  })

  const clearSelection = () => {
    if (cellsSelection.value) {
      cellsSelection.value = null
    }
    if (columnsSelection.value) {
      columnsSelection.value = null
    }
    if (rowsSelection.value) {
      rowsSelection.value = null
    }
  }

  const selectAllCells = () => {
    cellsSelection.value = {
      first: sheet.value.rows[0].cells[0],
      last: getRowLastCell(sheet.value.rows.at(-1))
    }
  }
  const getRowLastCell = (currentRow: RowDimensionType) => {
    for (const row of [...sheet.value.rows].reverse()) {
      if (
        row.cells.at(-1).relatedGlobalPositions.some((position: string) => {
          const { column, row } = parsePosition(position)
          return column === sheet.value.columns.at(-1).name && row === currentRow.globalIndex
        })
      ) {
        return row.cells.at(-1)
      }
    }
  }

  watch(cellsSelection, (newValue: SelectionType<CellType> | null) => {
    if (newValue) {
      rowsSelection.value = null
      columnsSelection.value = null
    }
  }, { deep: true })
  watch(columnsSelection, (newValue: SelectionType<ColumnDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      rowsSelection.value = null
      setActiveCell(null)
    }
  }, { deep: true })
  watch(rowsSelection, (newValue: SelectionType<RowDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      columnsSelection.value = null
      setActiveCell(null)
    }
  }, { deep: true })

  const mousedownCell = (cell: CellType): void => {
    selectionState.value = 'cell'
    cellsSelection.value = {
      first: cell,
      last: cell
    }
  }
  const mouseenterCell = (cell: CellType): void => {
    if (selectionState.value === 'cell') {
      cellsSelection.value.last = cell
    }
  }
  const mouseupCell = (cell: CellType): void => {
    if (selectionState.value === 'cell' && cellsSelection.value.first.id === cellsSelection.value.last.id) {
      setActiveCell(cell)
    }
  }

  const mouseenterColumnName = (column: ColumnDimensionType) => {
    if (selectionState.value === 'column') {
      columnsSelection.value.last = column
    }
  }

  const mouseDownColumnName = (column: ColumnDimensionType) => {
    selectionState.value = 'column'
    columnsSelection.value = {
      first: column,
      last: column
    }
  }

  const mouseenterRowName = (row: RowDimensionType) => {
    if (selectionState.value === 'row') {
      rowsSelection.value.last = row
    }
  }

  const mousedownRowName = (row: RowDimensionType) => {
    selectionState.value = 'row'
    rowsSelection.value = {
      first: row,
      last: row
    }
  }

  useEventListener('mouseup', () => {
    if (selectionState.value) {
      selectionState.value = null
    }
  })

  return {
    selectionState,
    allCellsSelected,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectionLines,
    selectedCellsOptions,
    selectedColumnDimensionsOptions,
    selectedRowDimensionsOptions,
    clearSelection,
    selectAllCells,
    mousedownCell,
    mouseenterCell,
    mouseupCell,
    mouseenterColumnName,
    mouseDownColumnName,
    mouseenterRowName,
    mousedownRowName
  }
}
