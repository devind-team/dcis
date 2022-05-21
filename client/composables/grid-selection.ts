import { useEventListener } from '@vueuse/core'
import { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  RangeIndicesType,
  GlobalSelectionType,
  Selection,
  CellOptionsType,
} from '~/types/grid'
import {
  parsePosition,
  positionsToRangeIndices,
  rangeIndicesToPositions,
  uniteCellsOptions
} from '~/services/grid'

export function useGridSelection (
  sheet: Ref<SheetType>,
  gridContainer: Ref<HTMLDivElement | null>,
  grid: Ref<HTMLTableElement | null>,
  setActiveCell: (cell: CellType) => void
) {
  const selectionState = ref<'cell' | 'column' | 'row' | null>(null)

  const getClearGlobalSelection = () => ({
    visible: false,
    position: { left: null, right: null, top: null, bottom: null },
    zIndex: 0,
    width: 0,
    height: 0
  })
  const globalSelection = ref<GlobalSelectionType>(getClearGlobalSelection())
  const clearGlobalSelection = () => {
    rowsSelection.value = null
    columnsSelection.value = null
    globalSelection.value = getClearGlobalSelection()
  }
  const setRowsGlobalSelection = () => {
    const indices = [rowsSelection.value.first.globalIndex, rowsSelection.value.last.globalIndex]
    const firstRow = grid.value.querySelector(
      `tbody tr:nth-child(${Math.min(...indices)})`
    ) as HTMLTableRowElement
    const firstRowCell = firstRow.cells.item(0)
    const lastRow = grid.value.querySelector(
      `tbody tr:nth-child(${Math.max(...indices)})`
    ) as HTMLTableRowElement
    const lastRowCell = lastRow.cells.item(0)
    globalSelection.value = {
      visible: true,
      position: {
        left: firstRowCell.offsetWidth,
        right: null,
        top: firstRowCell.offsetTop - 0.5,
        bottom: null
      },
      zIndex: gridContainer.value.scrollLeft ? 0 : 3,
      width: grid.value.offsetWidth - firstRowCell.offsetWidth,
      height: lastRow.offsetTop + lastRowCell.offsetHeight - firstRow.offsetTop + 1
    }
  }
  const setColumnsGlobalSelection = () => {
    const theadRow = grid.value.querySelector('thead tr') as HTMLTableRowElement
    const indices = [columnsSelection.value.first.index, columnsSelection.value.last.index]
    const firstColumn = theadRow.cells.item(Math.min(...indices)) as HTMLTableCellElement
    const lastColumn = theadRow.cells.item(Math.max(...indices)) as HTMLTableCellElement
    globalSelection.value = {
      visible: true,
      position: {
        left: firstColumn.offsetLeft - 0.5,
        right: null,
        top: firstColumn.offsetHeight - 1,
        bottom: null
      },
      zIndex: gridContainer.value.scrollTop ? 1 : 3,
      width: lastColumn.offsetLeft + lastColumn.offsetWidth - firstColumn.offsetLeft + 1,
      height: grid.value.offsetHeight - theadRow.offsetHeight + 1
    }
  }

  const cellsSelection = ref<Selection<CellType> | null>(null)
  const rowsSelection = ref<Selection<RowDimensionType> | null>(null)
  const columnsSelection = ref<Selection<ColumnDimensionType> | null>(null)

  watch(cellsSelection, (newValue: Selection<CellType> | null) => {
    if (newValue) {
      clearGlobalSelection()
    }
  }, { deep: true })
  watch(rowsSelection, (newValue: Selection<RowDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      columnsSelection.value = null
      setRowsGlobalSelection()
    }
  }, { deep: true })
  watch(columnsSelection, (newValue: Selection<ColumnDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      rowsSelection.value = null
      setColumnsGlobalSelection()
    }
  }, { deep: true })

  const gridContainerScroll = () => {
    if (rowsSelection.value) {
      setRowsGlobalSelection()
    }
    if (columnsSelection.value) {
      setColumnsGlobalSelection()
    }
  }

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
      const relatedPositions = selectedCells.reduce((a: string[], c: CellType) => {
        a.push(...c.relatedGlobalPositions)
        return a
      }, [])
      const selectedPositions = rangeIndicesToPositions(positionsToRangeIndices(relatedPositions))
      for (const row of sheet.value.rows) {
        for (const cell of row.cells) {
          for (const relatedPosition of cell.relatedGlobalPositions) {
            if (selectedPositions.includes(relatedPosition)) {
              newSelectedCells.push(cell)
            }
          }
        }
      }
    }
    return newSelectedCells
  })

  const selectedCellsPositions = computed<string[]>(() =>
    selectedCells.value.reduce((a: string[], c: CellType) => {
      a.push(...c.relatedGlobalPositions)
      return a
    }, []))
  const allCellsRangeIndices = computed<RangeIndicesType>(() => ({
    minColumn: 1,
    minRow: 1,
    maxColumn: sheet.value.columns.at(-1).index,
    maxRow: sheet.value.rows.at(-1).globalIndex
  }))
  const selectedRangeIndices = computed<RangeIndicesType | null>(() => {
    if (selectedCellsPositions.value.length) {
      return positionsToRangeIndices(selectedCellsPositions.value)
    }
    return null
  })
  const allCellsSelected = computed<boolean>(() => {
    if (selectedRangeIndices.value) {
      for (const [k, v] of Object.entries(selectedRangeIndices.value)) {
        if (allCellsRangeIndices.value[k] !== v) {
          return false
        }
      }
      return true
    }
    return false
  })

  const selectedColumnsPositions = computed<number[]>(() => {
    if (columnsSelection.value) {
      const indices = [
        columnsSelection.value.last.index,
        columnsSelection.value.first.index
      ]
      const minIndex = Math.min(...indices)
      const maxIndex = Math.max(...indices)
      return Array.from({
        length: maxIndex - minIndex + 1
      }).map((_, i) => i + minIndex)
    }
    if (selectedRangeIndices.value) {
      return Array.from({
        length: selectedRangeIndices.value.maxColumn - selectedRangeIndices.value.minColumn + 1
      }).map((_, i) => i + selectedRangeIndices.value.minColumn)
    }
    return []
  })
  const selectedRowsPositions = computed<number[]>(() => {
    if (rowsSelection.value) {
      const indices = [
        rowsSelection.value.last.globalIndex,
        rowsSelection.value.first.globalIndex
      ]
      const minIndex = Math.min(...indices)
      const maxIndex = Math.max(...indices)
      return Array.from({
        length: maxIndex - minIndex + 1
      }).map((_, i) => i + minIndex)
    }
    if (selectedRangeIndices.value) {
      return Array.from({
        length: selectedRangeIndices.value.maxRow - selectedRangeIndices.value.minRow + 1
      }).map((_, i) => i + selectedRangeIndices.value.minRow)
    }
    return []
  })

  const possibleCellsOptions: (keyof CellOptionsType)[] = [
    'kind', 'horizontalAlign', 'verticalAlign',
    'size', 'strong', 'italic',
    'strike', 'underline'
  ]
  const selectedCellsOptions = computed<CellOptionsType>(() => {
    const result: any = {}
    for (const option of possibleCellsOptions) {
      const options = []
      for (const cell of selectedCells.value) {
        options.push(cell[option])
      }
      result[option] = uniteCellsOptions(options)
    }
    return result
  })

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
  const selectAllCells = () => {
    cellsSelection.value = {
      first: sheet.value.rows[0].cells[0],
      last: getRowLastCell(sheet.value.rows.at(-1))
    }
  }

  useEventListener('mouseup', () => {
    if (selectionState.value) {
      selectionState.value = null
    }
  })

  return {
    selectionState,
    globalSelection,
    clearGlobalSelection,
    gridContainerScroll,
    selectedCellsPositions,
    allCellsSelected,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
    mousedownCell,
    mouseenterCell,
    mouseupCell,
    mouseenterColumnName,
    mouseDownColumnName,
    mouseenterRowName,
    mousedownRowName,
    selectAllCells
  }
}
