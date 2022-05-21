import { useEventListener } from '@vueuse/core'
import { Ref, UnwrapRef } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  ElementPositionType,
  ElementResizingType,
  GlobalSelectionType,
  ResizingType,
  BuildCellType,
  BuildColumnType,
  BuildRowType,
  Selection,
  CellOptionsType,
  BoundaryColumnCell,
  BoundaryRowCell, RangeIndicesType, MousePositionType
} from '~/types/grid'
import {
  parsePosition,
  positionsToRangeIndices,
  rangeIndicesToPositions,
  getCellStyle,
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
  } = useResizing<BuildColumnType, ColumnDimensionType>(
    gridContainer,
    64,
    'x',
    (buildColumn: BuildColumnType) => buildColumn.columnDimension,
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
  } = useResizing<BuildRowType, RowDimensionType>(
    gridContainer,
    25,
    'y',
    (buildRow: BuildRowType) => buildRow.rowDimension,
    changeRowHeight
  )
  watch(resizingRowHeight, (newValue: ElementResizingType) => {
    if (newValue.visible) {
      clearGlobalSelection()
    }
  }, { deep: true })

  const gridWidth = computed<number>(
    () => rowNameColumnWidth.value +
      columns.value.reduce((sum, column) => sum + getColumnWidth(column), 0)
  )

  /**
   * Структура для быстрого поиска колонок
   */
  const columnsMap = computed<Record<string, ColumnDimensionType>>(() =>
    sheet.value.columns.reduce((a, c: ColumnDimensionType) => ({ ...a, [c.id]: c }), {})
  )

  const rows = computed<BuildRowType[]>(() =>
    sheet.value.rows.map((rowDimension: RowDimensionType) => ({
      rowDimension,
      buildCells: rowDimension.cells.map((cell: CellType) => ({
        style: getCellStyle(cell),
        columnDimension: columnsMap.value[cell.columnId],
        rowDimension,
        cell
      }))
    }))
  )

  const columns = computed<BuildColumnType[]>(() =>
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => ({
      columnDimension
    }))
  )

  const selectionState = ref<'cell' | 'column' | 'row' | null>(null)

  const activeCell = ref<BuildCellType | null>(null)
  const setActiveCell = (buildCell: BuildCellType | null) => {
    activeCell.value = buildCell
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
    const indices = [
      rowsSelection.value.first.rowDimension.globalIndex,
      rowsSelection.value.last.rowDimension.globalIndex
    ]
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
    const indices = [
      columnsSelection.value.first.columnDimension.index,
      columnsSelection.value.last.columnDimension.index
    ]
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
      height: gridContainer.value.scrollHeight - theadRow.offsetHeight + 1
    }
  }

  const cellsSelection = ref<Selection<BuildCellType> | null>(null)
  const rowsSelection = ref<Selection<BuildRowType> | null>(null)
  const columnsSelection = ref<Selection<BuildColumnType> | null>(null)

  watch(cellsSelection, (newValue: Selection<BuildCellType> | null) => {
    if (newValue) {
      clearGlobalSelection()
    }
  }, { deep: true })
  watch(rowsSelection, (newValue: Selection<BuildRowType>) => {
    if (newValue) {
      cellsSelection.value = null
      columnsSelection.value = null
      setRowsGlobalSelection()
    }
  }, { deep: true })
  watch(columnsSelection, (newValue: Selection<BuildColumnType>) => {
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

  const selectedCells = computed<BuildCellType[]>(() => {
    if (!cellsSelection.value) {
      return []
    }
    let selectedCells = [cellsSelection.value.first, cellsSelection.value.last]
    let newSelectedCells: BuildCellType[] = []
    while (selectedCells.length !== newSelectedCells.length) {
      if (newSelectedCells.length) {
        selectedCells = newSelectedCells
        newSelectedCells = []
      }
      const relatedPositions = selectedCells.reduce((a: string[], c: BuildCellType) => {
        a.push(...c.cell.relatedGlobalPositions)
        return a
      }, [])
      const selectedPositions = rangeIndicesToPositions(positionsToRangeIndices(relatedPositions))
      for (const buildRow of rows.value) {
        for (const buildCell of buildRow.buildCells) {
          for (const relatedPosition of buildCell.cell.relatedGlobalPositions) {
            if (selectedPositions.includes(relatedPosition)) {
              newSelectedCells.push(buildCell)
            }
          }
        }
      }
    }
    return newSelectedCells
  })

  const selectedCellsPositions = computed<string[]>(() =>
    selectedCells.value.reduce((a: string[], c: BuildCellType) => {
      a.push(...c.cell.relatedGlobalPositions)
      return a
    }, []))
  const allCellsRangeIndices = computed<RangeIndicesType>(() => ({
    minColumn: 1,
    minRow: 1,
    maxColumn: columns.value.at(-1).columnDimension.index,
    maxRow: rows.value.at(-1).rowDimension.globalIndex
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
        columnsSelection.value.last.columnDimension.index,
        columnsSelection.value.first.columnDimension.index
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
        rowsSelection.value.last.rowDimension.globalIndex,
        rowsSelection.value.first.rowDimension.globalIndex
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
      for (const buildCell of selectedCells.value) {
        options.push(buildCell.cell[option])
      }
      result[option] = uniteCellsOptions(options)
    }
    return result
  })

  const mousedownCell = (buildCell: BuildCellType): void => {
    selectionState.value = 'cell'
    cellsSelection.value = {
      first: buildCell,
      last: buildCell
    }
  }
  const mouseenterCell = (buildCell: BuildCellType): void => {
    if (selectionState.value === 'cell') {
      cellsSelection.value.last = buildCell
    }
  }
  const mouseupCell = (buildCell: BuildCellType): void => {
    if (selectionState.value === 'cell' && cellsSelection.value.first.cell.id === cellsSelection.value.last.cell.id) {
      setActiveCell(buildCell)
    }
  }

  /**
   * Вычисление ячеек граничных к крайнему фиксированному столбцу
   */
  const boundaryColumnCells = computed<BoundaryColumnCell[]>(() => {
    const result: BoundaryColumnCell[] = []
    let i = 0
    while (i < rows.value.length) {
      const buildCell = rows.value[i].buildCells[0]
      result.push({ buildCell, buildRows: rows.value.slice(i, i + buildCell.cell.rowspan) })
      i += buildCell.cell.rowspan
    }
    return result
  })
  /**
   * Вычисление выделенных ячеек граничных к крайнему фиксированному столбцу
   */
  const selectedBoundaryColumnCells = computed<BoundaryColumnCell[]>(() =>
    boundaryColumnCells.value.filter(boundaryCell =>
      selectedCellsPositions.value.includes(boundaryCell.buildCell.cell.globalPosition))
  )

  /**
   * Вычисление ячеек граничных к крайней фиксированной строке
   */
  const boundaryRowCells = computed<BoundaryRowCell[]>(() => {
    const result: BoundaryRowCell[] = []
    let i = 0
    let offset = 0
    while (i < columns.value.length) {
      const buildCell = rows.value[0].buildCells[i - offset]
      result.push({ buildCell, buildColumns: columns.value.slice(i, i + buildCell.cell.colspan) })
      offset += buildCell.cell.colspan - 1
      i += buildCell.cell.colspan
    }
    return result
  })
  /**
   * Вычисление выделенных ячеек граничных к крайней фиксированной строке
   */
  const selectedBoundaryRowCells = computed<BoundaryRowCell[]>(() =>
    boundaryRowCells.value.filter(boundaryCell =>
      selectedCellsPositions.value.includes(boundaryCell.buildCell.cell.globalPosition))
  )

  const mouseenterColumnName = (buildColumn: BuildColumnType) => {
    if (selectionState.value === 'column') {
      columnsSelection.value.last = buildColumn
    }
  }
  const mousemoveColumnName = (buildColumn: BuildColumnType, event: MouseEvent) => {
    mousemoveColumnNameResizing(
      buildColumn,
      buildColumn.columnDimension.index - 1 > 0
        ? columns.value[buildColumn.columnDimension.index - 2]
        : null,
      event
    )
  }
  const mouseleaveColumnName = () => {
    mouseleaveColumnNameResizing()
  }
  const mousedownColumnName = (buildColumn: BuildColumnType, event: MouseEvent) => {
    if (resizingColumn.value) {
      mousedownColumnNameResizing(event)
    } else {
      selectionState.value = 'column'
      columnsSelection.value = {
        first: buildColumn,
        last: buildColumn
      }
    }
  }
  const mouseupColumnName = () => {
    mouseupColumnNameResizing()
  }

  const mouseenterRowName = (buildRow: BuildRowType) => {
    if (selectionState.value === 'row') {
      rowsSelection.value.last = buildRow
    }
  }
  const mousemoveRowName = (buildRow: BuildRowType, event: MouseEvent) => {
    mousemoveRowNameResizing(
      buildRow,
      buildRow.rowDimension.globalIndex - 1 > 0
        ? rows.value[buildRow.rowDimension.globalIndex - 2]
        : null,
      event
    )
  }
  const mouseleaveRowName = () => {
    mouseleaveRowNameResizing()
  }
  const mousedownRowName = (buildRow: BuildRowType, event: MouseEvent) => {
    if (resizingRow.value) {
      mousedownRowNameResizing(event)
    } else {
      selectionState.value = 'row'
      rowsSelection.value = {
        first: buildRow,
        last: buildRow
      }
    }
  }
  const mouseupRowName = () => {
    mouseupRowNameResizing()
  }

  const getRowLastBuildCell = (currentBuildRow: BuildRowType) => {
    for (const buildRow of [...rows.value].reverse()) {
      if (
        buildRow.buildCells.at(-1).cell.relatedGlobalPositions.some((position: string) => {
          const { column, row } = parsePosition(position)
          return column === sheet.value.columns.at(-1).name && row === currentBuildRow.rowDimension.globalIndex
        })
      ) {
        return buildRow.buildCells.at(-1)
      }
    }
  }
  const selectAllCells = () => {
    cellsSelection.value = {
      first: rows.value[0].buildCells[0],
      last: getRowLastBuildCell(rows.value.at(-1))
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
    rows,
    columns,
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

function useResizing<T, K extends { id: string, width?: number, height?: number }> (
  gridContainer: Ref<HTMLDivElement>,
  defaultSize: number,
  direction: 'x' | 'y',
  getDimension: (object: T) => K,
  changeSize: (object: K, size: number) => void
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

  const getSize = (object: T): number => {
    const dimension = getDimension(object)
    let size = 0
    if (resizing.value && getDimension(resizing.value.object as T).id === dimension.id) {
      size = resizing.value.size
    } else {
      size = dimension[dimensionKey] ? dimension[dimensionKey] : defaultElementSize.value
    }
    return size
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
      changeSize(getDimension(resizing.value.object as T), resizing.value.size)
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

  const setResizingHover = (object: T, mousePosition: MousePositionType) => {
    resizing.value = {
      object: object as UnwrapRef<T>,
      size: getDimension(object)[dimensionKey] ?? defaultElementSize.value,
      mousePosition,
      state: 'hover'
    }
  }

  useEventListener('mouseup', () => {
    if (resizing.value && resizing.value.state === 'resizing') {
      changeSize(getDimension(resizing.value.object as T), resizing.value.size)
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
