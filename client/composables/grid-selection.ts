import { useEventListener } from '@vueuse/core'
import { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  RangeIndicesType,
  SelectionViewType,
  SelectionType,
  CellOptionsType
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

  const getClearGlobalSelectionView = (): SelectionViewType => ({
    id: '0',
    visible: false,
    position: { left: null, right: null, top: null, bottom: null },
    zIndex: 0,
    width: 0,
    height: 0,
    border: { top: false, right: false, bottom: false, left: false }
  })
  const globalSelectionView = ref<SelectionViewType>(getClearGlobalSelectionView())
  const clearGlobalSelectionView = () => {
    rowsSelection.value = null
    columnsSelection.value = null
    globalSelectionView.value = getClearGlobalSelectionView()
  }
  const setGlobalSelectionView = (left: number, top: number, zIndex: number, width: number, height: number) => {
    globalSelectionView.value = {
      id: '0',
      visible: true,
      position: { left, right: null, top, bottom: null },
      zIndex,
      width,
      height,
      border: { top: true, right: true, bottom: true, left: true }
    }
  }
  const setRowsGlobalSelectionView = () => {
    const indices = [rowsSelection.value.first.globalIndex, rowsSelection.value.last.globalIndex]
    const firstRow = grid.value.querySelector(
      `tbody tr:nth-child(${Math.min(...indices)})`
    ) as HTMLTableRowElement
    const firstRowCell = firstRow.cells.item(0)
    const lastRow = grid.value.querySelector(
      `tbody tr:nth-child(${Math.max(...indices)})`
    ) as HTMLTableRowElement
    const lastRowCell = lastRow.cells.item(0)
    setGlobalSelectionView(
      firstRowCell.offsetWidth - 1,
      firstRowCell.offsetTop - 1,
      gridContainer.value.scrollLeft ? 0 : 3,
      grid.value.offsetWidth - firstRowCell.offsetWidth + 1,
      lastRow.offsetTop + lastRowCell.offsetHeight - firstRow.offsetTop + 1
    )
  }
  const setColumnsGlobalSelectionView = () => {
    const theadRow = grid.value.querySelector('thead tr') as HTMLTableRowElement
    const indices = [columnsSelection.value.first.index, columnsSelection.value.last.index]
    const firstColumn = theadRow.cells.item(Math.min(...indices)) as HTMLTableCellElement
    const lastColumn = theadRow.cells.item(Math.max(...indices)) as HTMLTableCellElement
    setGlobalSelectionView(
      firstColumn.offsetLeft - 1,
      firstColumn.offsetHeight - 1,
      gridContainer.value.scrollTop ? 1 : 3,
      lastColumn.offsetLeft + lastColumn.offsetWidth - firstColumn.offsetLeft + 1,
      grid.value.offsetHeight - theadRow.offsetHeight + 1
    )
  }

  const cellsSelection = ref<SelectionType<CellType> | null>(null)
  const rowsSelection = ref<SelectionType<RowDimensionType> | null>(null)
  const columnsSelection = ref<SelectionType<ColumnDimensionType> | null>(null)

  watch(cellsSelection, (newValue: SelectionType<CellType> | null) => {
    if (newValue) {
      clearGlobalSelectionView()
    }
  }, { deep: true })
  watch(rowsSelection, (newValue: SelectionType<RowDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      columnsSelection.value = null
      setRowsGlobalSelectionView()
    }
  }, { deep: true })
  watch(columnsSelection, (newValue: SelectionType<ColumnDimensionType>) => {
    if (newValue) {
      cellsSelection.value = null
      rowsSelection.value = null
      setColumnsGlobalSelectionView()
    }
  }, { deep: true })

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
    return newSelectedCells.reduce(
      (acc: CellType[], cell: CellType) => acc.find((c: CellType) => c.id === cell.id) ? acc : [...acc, cell],
      []
    )
  })
  const selectionView = ref<SelectionViewType[]>([])
  const setSelectionView = (selectedCells: CellType[]) => {
    if (selectedCells.length) {
      const result: SelectionViewType[] = []
      const theadRow = grid.value.querySelector('thead tr') as HTMLTableRowElement
      const { leftColumn, topRow } = getSelectionViewLeftTopBorder(selectedCells)
      for (const cell of selectedCells) {
        const { minColumn, minRow, maxColumn, maxRow } = positionsToRangeIndices(cell.relatedGlobalPositions)
        const firstColumn = theadRow.cells.item(minColumn) as HTMLTableCellElement
        const lastColumn = theadRow.cells.item(maxColumn) as HTMLTableCellElement
        const firstRow = grid.value.querySelector(`tbody tr:nth-child(${minRow})`) as HTMLTableRowElement
        const firstRowCell = firstRow.cells.item(0)
        const lastRow = grid.value.querySelector(`tbody tr:nth-child(${maxRow})`) as HTMLTableRowElement
        const lastRowCell = lastRow.cells.item(0)
        result.push({
          id: cell.id,
          visible: true,
          position: { left: firstColumn.offsetLeft - 1, right: null, top: firstRowCell.offsetTop - 1, bottom: null },
          zIndex: 2,
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
      selectionView.value = result
    } else {
      selectionView.value = null
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
  watch(selectedCells, (newValue: CellType[]) => setSelectionView(newValue))

  const gridContainerScroll = () => {
    if (cellsSelection.value) {
      setSelectionView(selectedCells.value)
    }
    if (rowsSelection.value) {
      setRowsGlobalSelectionView()
    }
    if (columnsSelection.value) {
      setColumnsGlobalSelectionView()
    }
  }

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

  const boundarySelectedColumnsPositions = computed<number[]>(() => {
    const result: number[] = []
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
  const boundarySelectedRowsRowsPositions = computed<number[]>(() => {
    const result: number[] = []
    let i = 0
    while (i < sheet.value.rows.length) {
      const cell = sheet.value.rows[i].cells[0]
      if (selectedCellsPositions.value.includes(cell.globalPosition)) {
        result.push(...sheet.value.rows.slice(i, i + cell.rowspan).map((row: RowDimensionType) => row.globalIndex))
      }
      i += cell.rowspan
    }
    return result
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

  useEventListener('mouseup', () => {
    if (selectionState.value) {
      selectionState.value = null
    }
  })

  return {
    selectionState,
    globalSelectionView,
    clearGlobalSelectionView,
    gridContainerScroll,
    selectionView,
    allCellsSelected,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
    boundarySelectedColumnsPositions,
    boundarySelectedRowsRowsPositions,
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
