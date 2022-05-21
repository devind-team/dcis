import { useEventListener } from '@vueuse/core'
import { Ref, UnwrapRef } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  ElementPositionType,
  ElementResizingType,
  GlobalSelectionType,
  ResizingType,
  Selection,
  CellOptionsType,
  BoundaryColumnCell,
  BoundaryRowCell, RangeIndicesType, MousePositionType
} from '~/types/grid'
import {
  parsePosition,
  positionsToRangeIndices,
  rangeIndicesToPositions,
  uniteCellsOptions
} from '~/services/grid'

export const cellKinds = {
  n: 'Numeric',
  s: 'String',
  text: 'Text',
  fl: 'Files',
  money: 'Money',
  department: 'Department',
  classification: 'Classification'
}

export function useGrid (
  sheet: Ref<SheetType>,
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => void,
  changeRowHeight: (rowDimension: RowDimensionType, height: number) => void
) {
  const rowNameColumnWidth = computed<number>(() => {
    let maxDigits = 0
    let maxDots = 0
    for (const row of sheet.value.rows) {
      const indices = row.name.split('.')
      const dots = indices.length - 1
      if (dots > maxDots) {
        maxDots = dots
      }
      const digits = row.name.length - dots
      if (digits > maxDigits) {
        maxDigits = digits
      }
    }
    return maxDigits * 11 + maxDots * 2 + 10
  })
  const gridContainer = ref<HTMLDivElement | null>(null)
  const grid = ref<HTMLTableElement | null>(null)

  const {
    resizing: resizingColumn,
    elementResizing: resizingColumnWidth,
    getSize: getColumnWidth,
    mousemove: mousemoveColumnNameResizing,
    mouseleave: mouseleaveColumnNameResizing,
    mousedown: mousedownColumnNameResizing,
    mouseup: mouseupColumnNameResizing
  } = useResizing<ColumnDimensionType>(
    gridContainer,
    64,
    'x',
    changeColumnWidth
  )
  watch(resizingColumnWidth, (newValue: ElementResizingType) => {
    if (newValue.visible) {
      clearGlobalSelection()
    }
  }, { deep: true })
  const {
    resizing: resizingRow,
    elementResizing: resizingRowHeight,
    getSize: getRowHeight,
    mousemove: mousemoveRowNameResizing,
    mouseleave: mouseleaveRowNameResizing,
    mousedown: mousedownRowNameResizing,
    mouseup: mouseupRowNameResizing
  } = useResizing<RowDimensionType>(
    gridContainer,
    25,
    'y',
    changeRowHeight
  )
  watch(resizingRowHeight, (newValue: ElementResizingType) => {
    if (newValue.visible) {
      clearGlobalSelection()
    }
  }, { deep: true })

  const gridWidth = computed<number>(
    () => rowNameColumnWidth.value +
      sheet.value.columns.reduce((sum: number, column: ColumnDimensionType) => sum + getColumnWidth(column), 0)
  )

  const selectionState = ref<'cell' | 'column' | 'row' | null>(null)

  const activeCell = ref<CellType | null>(null)
  const setActiveCell = (cell: CellType | null) => {
    activeCell.value = cell
  }

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

  /**
   * Вычисление ячеек граничных к крайнему фиксированному столбцу
   */
  const boundaryColumnCells = computed<BoundaryColumnCell[]>(() => {
    const result: BoundaryColumnCell[] = []
    let i = 0
    while (i < sheet.value.rows.length) {
      const cell = sheet.value.rows[i].cells[0]
      result.push({ cell, rows: sheet.value.rows.slice(i, i + cell.rowspan) })
      i += cell.rowspan
    }
    return result
  })
  /**
   * Вычисление выделенных ячеек граничных к крайнему фиксированному столбцу
   */
  const selectedBoundaryColumnCells = computed<BoundaryColumnCell[]>(() =>
    boundaryColumnCells.value.filter(boundaryCell =>
      selectedCellsPositions.value.includes(boundaryCell.cell.globalPosition))
  )

  /**
   * Вычисление ячеек граничных к крайней фиксированной строке
   */
  const boundaryRowCells = computed<BoundaryRowCell[]>(() => {
    const result: BoundaryRowCell[] = []
    let i = 0
    let offset = 0
    while (i < sheet.value.columns.length) {
      const cell = sheet.value.rows[0].cells[i - offset]
      result.push({ cell, columns: sheet.value.columns.slice(i, i + cell.colspan) })
      offset += cell.colspan - 1
      i += cell.colspan
    }
    return result
  })
  /**
   * Вычисление выделенных ячеек граничных к крайней фиксированной строке
   */
  const selectedBoundaryRowCells = computed<BoundaryRowCell[]>(() =>
    boundaryRowCells.value.filter(boundaryCell =>
      selectedCellsPositions.value.includes(boundaryCell.cell.globalPosition))
  )

  const mouseenterColumnName = (column: ColumnDimensionType) => {
    if (selectionState.value === 'column') {
      columnsSelection.value.last = column
    }
  }
  const mousemoveColumnName = (column: ColumnDimensionType, event: MouseEvent) => {
    mousemoveColumnNameResizing(
      column,
      column.index - 1 > 0
        ? sheet.value.columns[column.index - 2]
        : null,
      event
    )
  }
  const mouseleaveColumnName = () => {
    mouseleaveColumnNameResizing()
  }
  const mousedownColumnName = (column: ColumnDimensionType, event: MouseEvent) => {
    if (resizingColumn.value) {
      mousedownColumnNameResizing(event)
    } else {
      selectionState.value = 'column'
      columnsSelection.value = {
        first: column,
        last: column
      }
    }
  }
  const mouseupColumnName = () => {
    mouseupColumnNameResizing()
  }

  const mouseenterRowName = (row: RowDimensionType) => {
    if (selectionState.value === 'row') {
      rowsSelection.value.last = row
    }
  }
  const mousemoveRowName = (row: RowDimensionType, event: MouseEvent) => {
    mousemoveRowNameResizing(
      row,
      row.globalIndex - 1 > 0
        ? sheet.value.rows[row.globalIndex - 2]
        : null,
      event
    )
  }
  const mouseleaveRowName = () => {
    mouseleaveRowNameResizing()
  }
  const mousedownRowName = (row: RowDimensionType, event: MouseEvent) => {
    if (resizingRow.value) {
      mousedownRowNameResizing(event)
    } else {
      selectionState.value = 'row'
      rowsSelection.value = {
        first: row,
        last: row
      }
    }
  }
  const mouseupRowName = () => {
    mouseupRowNameResizing()
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

  /**
   * Класс курсора на странице
   */
  const cursorClass = computed<
    'grid__cursor_cell' | 'grid__cursor_col-resize' | 'grid__cursor_row-resize' | null
  >(() => {
    if (selectionState.value) {
      return 'grid__cursor_cell'
    }
    if (resizingColumn.value) {
      return 'grid__cursor_col-resize'
    }
    if (resizingRow.value) {
      return 'grid__cursor_row-resize'
    }
    return null
  })
  useOverlyingClass(document.body, cursorClass)

  useEventListener('mouseup', () => {
    if (selectionState.value) {
      selectionState.value = null
    }
  })

  return {
    gridContainer,
    grid,
    resizingColumn,
    resizingColumnWidth,
    getColumnWidth,
    resizingRow,
    resizingRowHeight,
    getRowHeight,
    gridWidth,
    rowNameColumnWidth,
    activeCell,
    setActiveCell,
    allCellsSelected,
    selectedCellsPositions,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
    globalSelection,
    gridContainerScroll,
    mousedownCell,
    mouseenterCell,
    mouseupCell,
    boundaryColumnCells,
    selectedBoundaryColumnCells,
    boundaryRowCells,
    selectedBoundaryRowCells,
    mouseenterColumnName,
    mousemoveColumnName,
    mouseleaveColumnName,
    mousedownColumnName,
    mouseupColumnName,
    mouseenterRowName,
    mousemoveRowName,
    mouseleaveRowName,
    mousedownRowName,
    mouseupRowName,
    selectAllCells
  }
}

function useResizing<T extends { id: string, width?: number, height?: number }> (
  gridContainer: Ref<HTMLDivElement>,
  defaultSize: number,
  direction: 'x' | 'y',
  changeSize: (object: T, size: number) => void
) {
  const borderGag = 6

  const dimensionKey = direction === 'x' ? 'width' : 'height'
  const offsetSizeKey = direction === 'x' ? 'offsetWidth' : 'offsetHeight'
  const eventOffsetKey = direction === 'x' ? 'offsetX' : 'offsetY'

  const defaultElementSize = ref<number>(defaultSize)
  const resizing = ref<ResizingType<T> | null>(null)
  const elementPosition = ref<ElementPositionType>({ left: null, right: null, top: null, bottom: null })
  const elementResizing = computed<ElementResizingType>(() => ({
    visible: !!resizing.value && resizing.value.state === 'resizing',
    position: elementPosition.value,
    size: resizing.value ? resizing.value.size : 0
  }))

  const getSize = (dimension: T): number => {
    if (resizing.value && resizing.value.object.id === dimension.id) {
      return resizing.value.size
    } else {
      return dimension[dimensionKey] ? dimension[dimensionKey] : defaultElementSize.value
    }
  }

  const mousemove = (object: T, previousObject: T | null, event: MouseEvent) => {
    const mousePosition = { x: event.clientX, y: event.clientY }
    const cell = event.target as HTMLTableCellElement
    if (resizing.value && resizing.value.state === 'resizing') {
      resizing.value.size = Math.max(
        resizing.value.size + mousePosition[direction] - resizing.value.mousePosition[direction], 0
      )
      resizing.value.mousePosition = mousePosition
    } else if (cell[offsetSizeKey] - event[eventOffsetKey] < borderGag) {
      setResizingHover(object, mousePosition)
    } else if (
      cell[offsetSizeKey] - event[eventOffsetKey] > cell[offsetSizeKey] - borderGag &&
      previousObject
    ) {
      setResizingHover(previousObject, mousePosition)
    } else {
      resizing.value = null
    }
  }

  const mouseleave = () => {
    if (resizing.value && resizing.value.state === 'hover') {
      resizing.value = null
    }
  }

  const mousedown = (event: MouseEvent) => {
    if (resizing.value) {
      const target = event.target as HTMLDivElement | HTMLTableCellElement
      if (direction === 'x') {
        elementPosition.value = getElementPositionX(event, target)
      } else {
        elementPosition.value = getElementPositionY(event, target)
      }
      resizing.value.state = 'resizing'
    }
  }

  const mouseup = () => {
    if (resizing.value) {
      changeSize(resizing.value.object as T, resizing.value.size)
      resizing.value.state = 'hover'
    }
  }

  const getElementPositionX = (event: MouseEvent, target: HTMLDivElement | HTMLTableCellElement) => {
    if (
      target.offsetLeft - gridContainer.value.scrollLeft +
      event.offsetX < document.body[offsetSizeKey] - 150
    ) {
      return {
        left: target.offsetLeft - gridContainer.value.scrollLeft + event.offsetX,
        right: null,
        top: target.offsetTop + event.offsetY - 25,
        bottom: null
      }
    } else {
      return {
        left: null,
        right: 25,
        top: target.offsetTop + event.offsetY - 25,
        bottom: null
      }
    }
  }

  const getElementPositionY = (event: MouseEvent, target: HTMLDivElement | HTMLTableCellElement) => {
    const row = target.closest('tr')
    return {
      left: target.offsetLeft + event.offsetX,
      right: null,
      top: row.offsetTop - gridContainer.value.scrollTop + event.offsetY - 25,
      bottom: null
    }
  }

  const setResizingHover = (dimension: T, mousePosition: MousePositionType) => {
    resizing.value = {
      object: dimension as UnwrapRef<T>,
      size: dimension[dimensionKey] ?? defaultElementSize.value,
      mousePosition,
      state: 'hover'
    }
  }

  useEventListener('mouseup', () => {
    if (resizing.value && resizing.value.state === 'resizing') {
      changeSize(resizing.value.object as T, resizing.value.size)
      resizing.value = null
    }
  })

  useEventListener('mousemove', (event: MouseEvent) => {
    if (resizing.value && resizing.value.state === 'resizing') {
      const mousePosition = { x: event.clientX, y: event.clientY }
      resizing.value.size = Math.max(
        resizing.value.size + mousePosition[direction] - resizing.value.mousePosition[direction], 0
      )
      resizing.value.mousePosition = mousePosition
    }
  })

  return {
    resizing,
    elementResizing,
    getSize,
    mousemove,
    mouseleave,
    mousedown,
    mouseup
  }
}
