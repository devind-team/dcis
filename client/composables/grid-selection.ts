import { useEventListener } from '@vueuse/core'
import { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  RangeIndicesType,
  SelectionType,
  SelectionViewType,
  ScrollInfoType,
  CellsOptionsType,
  ColumnDimensionsOptionsType,
  RowDimensionsOptionsType
} from '~/types/grid'
import {
  parsePosition,
  positionsToRangeIndices,
  rangeIndicesToPositions,
  filterCells,
  findCell,
  getRelatedGlobalPositions,
  getCellOptions,
  getColumnDimensionsOptions,
  getRowDimensionsOptions
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

  const cellsSelectionView = ref<SelectionViewType[] | null>(null)
  const columnsSelectionView = ref<SelectionViewType | null>(null)
  const rowsSelectionView = ref<SelectionViewType | null>(null)

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

  const selectedCellsOptions = computed<CellsOptionsType | null>(() => {
    if (cellsSelection.value) {
      return getCellOptions(selectedCells.value)
    }
    if (rowsSelection.value) {
      return getCellOptions(selectedRowsCells.value)
    }
    if (columnsSelection.value) {
      return getCellOptions(selectedColumnsCells.value)
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

  const updateSelectionViews = () => {
    nextTick(() => {
      updateCellsSelectionView()
      updateColumnsSelectionView()
      updateRowsSelectionView()
    })
  }
  const updateCellsSelectionView = () => {
    if (cellsSelection.value) {
      cellsSelectionView.value = []
      const theadRow = grid.value.querySelector('thead tr') as HTMLTableRowElement
      const { leftColumn, topRow } = getSelectionViewLeftTopBorder(selectedCells.value)
      for (const cell of selectedCells.value) {
        const { minColumn, minRow, maxColumn, maxRow } = positionsToRangeIndices(cell.relatedGlobalPositions)
        const firstColumn = theadRow.cells.item(minColumn) as HTMLTableCellElement
        const lastColumn = theadRow.cells.item(maxColumn) as HTMLTableCellElement
        const firstRow = grid.value.querySelector(`tbody tr:nth-child(${minRow})`) as HTMLTableRowElement
        const firstRowCell = firstRow.cells.item(0)
        const lastRow = grid.value.querySelector(`tbody tr:nth-child(${maxRow})`) as HTMLTableRowElement
        const lastRowCell = lastRow.cells.item(0)
        cellsSelectionView.value.push({
          id: cell.id,
          position: { left: firstColumn.offsetLeft - 1, right: null, top: firstRowCell.offsetTop - 1, bottom: null },
          width: lastColumn.offsetLeft + lastColumn.offsetWidth - firstColumn.offsetLeft + 1,
          height: lastRow.offsetTop + lastRowCell.offsetHeight - firstRow.offsetTop + 1,
          border: {
            top: minRow !== 1 && minRow === topRow,
            right: true,
            bottom: true,
            left: minColumn !== 1 && minColumn === leftColumn
          }
        })
      }
    } else {
      cellsSelectionView.value = null
    }
  }
  const boundarySelectedColumnsPositions = computed<number[]>(() => {
    if (scroll.value.top) {
      return []
    }
    if (
      rowsSelection.value &&
      [rowsSelection.value.first.globalIndex, rowsSelection.value.last.globalIndex].includes(1)
    ) {
      return sheet.value.columns.map((column: ColumnDimensionType) => column.index)
    }
    if (columnsSelection.value) {
      return selectedColumnsPositions.value
    }
    const result = []
    let i = 0
    let offset = 0
    while (i < sheet.value.columns.length) {
      const cell = sheet.value.rows[0].cells[i - offset]
      if (selectedCellsPositions.value.includes(cell.globalPosition)) {
        result.push(...sheet.value.columns.slice(i, i + cell.colspan)
          .map((column: ColumnDimensionType) => column.index)
        )
      }
      offset += cell.colspan - 1
      i += cell.colspan
    }
    return result
  })
  const boundarySelectedRowsPositions = computed<number[]>(() => {
    if (scroll.value.left) {
      return []
    }
    if (rowsSelection.value) {
      return selectedRowsPositions.value
    }
    if (
      columnsSelection.value &&
      [columnsSelection.value.first.index, columnsSelection.value.last.index].includes(1)
    ) {
      return sheet.value.rows.map((row: RowDimensionType) => row.globalIndex)
    }
    const result: number[] = []
    let i = 0
    while (i < sheet.value.rows.length) {
      const cell = sheet.value.rows[i].cells[0]
      if (selectedCellsPositions.value.includes(cell.globalPosition)) {
        result.push(...sheet.value.rows.slice(i, i + cell.rowspan)
          .map((row: RowDimensionType) => row.globalIndex))
      }
      i += cell.rowspan
    }
    return result
  })
  const updateColumnsSelectionView = () => {
    if (columnsSelection.value) {
      const theadRow = grid.value.querySelector('thead tr') as HTMLTableRowElement
      const indices = [columnsSelection.value.first.index, columnsSelection.value.last.index]
      const firstColumnIndex = Math.min(...indices)
      const firstColumn = theadRow.cells.item(firstColumnIndex) as HTMLTableCellElement
      const lastColumn = theadRow.cells.item(Math.max(...indices)) as HTMLTableCellElement
      columnsSelectionView.value = {
        id: 'column',
        position: { left: firstColumn.offsetLeft - 1, right: null, top: firstColumn.offsetHeight - 1, bottom: null },
        width: lastColumn.offsetLeft + lastColumn.offsetWidth - firstColumn.offsetLeft + 1,
        height: grid.value.offsetHeight - theadRow.offsetHeight + 1,
        border: { top: false, right: true, bottom: true, left: firstColumnIndex !== 1 }
      }
    } else {
      columnsSelectionView.value = null
    }
  }
  const updateRowsSelectionView = () => {
    if (rowsSelection.value) {
      const indices = [rowsSelection.value.first.globalIndex, rowsSelection.value.last.globalIndex]
      const firstRowIndex = Math.min(...indices)
      const firstRow = grid.value.querySelector(
        `tbody tr:nth-child(${firstRowIndex})`
      ) as HTMLTableRowElement
      const firstRowCell = firstRow.cells.item(0)
      const lastRow = grid.value.querySelector(
        `tbody tr:nth-child(${Math.max(...indices)})`
      ) as HTMLTableRowElement
      const lastRowCell = lastRow.cells.item(0)
      rowsSelectionView.value = {
        id: 'row',
        position: { left: firstRowCell.offsetWidth - 1, right: null, top: firstRowCell.offsetTop - 1, bottom: null },
        width: grid.value.offsetWidth - firstRowCell.offsetWidth + 1,
        height: lastRow.offsetTop + lastRowCell.offsetHeight - firstRow.offsetTop + 1,
        border: { top: firstRowIndex !== 1, right: true, bottom: true, left: false }
      }
    } else {
      rowsSelectionView.value = null
    }
  }
  const getSelectionViewLeftTopBorder = (selectedCells: CellType[]): { leftColumn: number, topRow: number} => {
    let leftColumn = Number.MAX_VALUE
    let topRow = Number.MAX_VALUE
    for (const cell of selectedCells) {
      const { minColumn, minRow } = positionsToRangeIndices(cell.relatedGlobalPositions)
      if (minColumn < leftColumn) {
        leftColumn = minColumn
      }
      if (minRow < topRow) {
        topRow = minRow
      }
    }
    return { leftColumn, topRow }
  }

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
    updateSelectionViews()
  }

  const selectSelectionCell = (cell: CellType) => {
    cellsSelection.value = {
      first: cell,
      last: cell
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
      updateSelectionViews()
    }
  }, { deep: true })
  watch(columnsSelection, (newValue: SelectionType<ColumnDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      rowsSelection.value = null
      setActiveCell(null)
      updateSelectionViews()
    }
  }, { deep: true })
  watch(rowsSelection, (newValue: SelectionType<RowDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      columnsSelection.value = null
      setActiveCell(null)
      updateSelectionViews()
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
    selectedCells,
    cellsSelectionView,
    rowsSelectionView,
    columnsSelectionView,
    boundarySelectedColumnsPositions,
    boundarySelectedRowsPositions,
    allCellsSelected,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
    selectedColumnDimensionsOptions,
    selectedRowDimensionsOptions,
    updateSelectionViews,
    clearSelection,
    selectAllCells,
    mousedownCell,
    mouseenterCell,
    mouseupCell,
    mouseenterColumnName,
    mouseDownColumnName,
    mouseenterRowName,
    mousedownRowName,
    selectSelectionCell
  }
}
