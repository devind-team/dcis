import { useEventListener } from '@vueuse/core'
import { Ref, UnwrapRef } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  ElementPositionType,
  ElementSizeType,
  ResitingType,
  BuildCellType,
  BuildColumnType,
  BuildRowType,
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
  const gridWidth = computed<number>(
    () => rowNameColumnWidth.value +
      columns.value.reduce((sum, column) => sum + column.width, 0)
  )

  const {
    resizing: resizingColumn,
    elementSize: columnWidth,
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
  const {
    resizing: resizingRow,
    elementSize: rowHeight,
    getSize: getRowHeight,
    mousemove: mousemoveRowNameResizing,
    mouseleave: mouseleaveRowNameResizing,
    mousedown: mousedownRowNameResizing,
    mouseup: mouseupRowNameResizing
  } = useResizing<BuildRowType, RowDimensionType>(
    gridContainer,
    16,
    'y',
    (buildRow: BuildRowType) => buildRow.rowDimension,
    changeRowHeight
  )

  /**
   * Структура для быстрого поиска колонок
   */
  const columnsMap = computed<Record<string, ColumnDimensionType>>(() =>
    sheet.value.columns.reduce((a, c: ColumnDimensionType) => ({ ...a, [c.id]: c }), {})
  )

  const assignRowFirstBuildCell = (buildRows: BuildRowType[], currentBuildRow: BuildRowType) => {
    for (const buildRow of buildRows) {
      if (
        buildRow.buildCells[0].cell.relatedGlobalPositions.some((position: string) => {
          const { column, row } = parsePosition(position)
          return column === 'A' && row === currentBuildRow.rowDimension.globalIndex
        })
      ) {
        currentBuildRow.firstBuildCell = buildRow.buildCells[0]
        return
      }
    }
  }
  const assignRowLastBuildCell = (buildRows: BuildRowType[], currentBuildRow: BuildRowType) => {
    for (const buildRow of buildRows) {
      if (
        buildRow.buildCells.at(-1).cell.relatedGlobalPositions.some((position: string) => {
          const { column, row } = parsePosition(position)
          return column === sheet.value.columns.at(-1).name && row === currentBuildRow.rowDimension.globalIndex
        })
      ) {
        currentBuildRow.lastBuildCell = buildRow.buildCells.at(-1)
      }
    }
  }
  const rows = computed<BuildRowType[]>(() => {
    const buildRows = sheet.value.rows.map((rowDimension: RowDimensionType) => {
      const height = getRowHeight(rowDimension)
      return {
        style: { height: `${height}px` },
        height,
        rowDimension,
        buildCells: rowDimension.cells.map((cell: CellType) => ({
          style: getCellStyle(cell),
          columnDimension: columnsMap.value[cell.columnId],
          rowDimension,
          cell
        })),
        firstBuildCell: null,
        lastBuildCell: null
      }
    })
    for (const currentBuildRow of buildRows) {
      assignRowFirstBuildCell(buildRows, currentBuildRow)
      assignRowLastBuildCell(buildRows, currentBuildRow)
    }
    return buildRows
  })

  const assignColumnFirstBuildCell = (currentBuildColumn: BuildColumnType) => {
    for (const buildCell of rows.value[0].buildCells) {
      if (
        buildCell.cell.relatedGlobalPositions.some((position: string) => {
          const { column } = parsePosition(position)
          return column === currentBuildColumn.columnDimension.name
        })
      ) {
        currentBuildColumn.firstBuildCell = buildCell
        return
      }
    }
  }
  const assignColumnLastBuildCell = (currentBuildColumn: BuildColumnType) => {
    for (const buildRow of [...rows.value].reverse()) {
      for (const buildCell of buildRow.buildCells) {
        if (
          buildCell.cell.relatedGlobalPositions.some((position: string) => {
            const { column } = parsePosition(position)
            return column === currentBuildColumn.columnDimension.name
          })
        ) {
          currentBuildColumn.lastBuildCell = buildCell
          return
        }
      }
    }
  }
  const columns = computed<BuildColumnType[]>(() => {
    const buildColumns = sheet.value.columns.map((columnDimension: ColumnDimensionType) => {
      const width = getColumnWidth(columnDimension)
      return {
        style: { width: `${width}px` },
        width,
        columnDimension,
        firstBuildCell: null,
        lastBuildCell: null
      }
    })
    for (const currentBuildColumn of buildColumns) {
      assignColumnFirstBuildCell(currentBuildColumn)
      assignColumnLastBuildCell(currentBuildColumn)
    }
    return buildColumns
  })

  const selectionState = ref<'cell' | 'column' | 'row' | null>(null)

  const activeCell = ref<BuildCellType | null>(null)
  const setActiveCell = (buildCell: BuildCellType | null) => {
    activeCell.value = buildCell
  }

  const selection = ref<{ first: BuildCellType, last: BuildCellType } | null>(null)
  const selectedCells = computed<BuildCellType[]>(() => {
    if (!selection.value) {
      return []
    }
    let selectedCells = [selection.value.first, selection.value.last]
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
    if (selectedRangeIndices.value) {
      return Array.from({
        length: selectedRangeIndices.value.maxColumn - selectedRangeIndices.value.minColumn + 1
      }).map((_, i) => i + selectedRangeIndices.value.minColumn)
    }
    return []
  })
  const selectedRowsPositions = computed<number[]>(() => {
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
    selection.value = {
      first: buildCell,
      last: buildCell
    }
  }
  const mouseenterCell = (buildCell: BuildCellType): void => {
    if (selectionState.value === 'cell') {
      selection.value.last = buildCell
    }
  }
  const mouseupCell = (buildCell: BuildCellType): void => {
    if (selectionState.value === 'cell' && selection.value.first.cell.id === selection.value.last.cell.id) {
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
      selection.value.last = buildColumn.lastBuildCell
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
      selection.value = {
        first: buildColumn.firstBuildCell,
        last: buildColumn.lastBuildCell
      }
    }
  }
  const mouseupColumnName = () => {
    mouseupColumnNameResizing()
  }

  const mouseenterRowName = (buildRow: BuildRowType) => {
    if (selectionState.value === 'row') {
      selection.value.last = buildRow.lastBuildCell
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
      selection.value = {
        first: buildRow.firstBuildCell,
        last: buildRow.lastBuildCell
      }
    }
  }
  const mouseupRowName = () => {
    mouseupRowNameResizing()
  }

  const selectAllCells = () => {
    selection.value = {
      first: rows.value[0].firstBuildCell,
      last: rows.value.at(-1).lastBuildCell
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
    columnWidth,
    rowHeight,
    rows,
    columns,
    rowNameColumnWidth,
    gridContainer,
    gridWidth,
    activeCell,
    setActiveCell,
    allCellsSelected,
    selectedCellsPositions,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
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
  const borderGag = 10

  const dimensionKey = direction === 'x' ? 'width' : 'height'
  const offsetSizeKey = direction === 'x' ? 'offsetWidth' : 'offsetHeight'
  const eventOffsetKey = direction === 'x' ? 'offsetX' : 'offsetY'

  const defaultElementSize = ref<number>(defaultSize)
  const resizing = ref<ResitingType<T> | null>(null)
  const elementPosition = ref<ElementPositionType>({ left: null, right: null, top: null, bottom: null })
  const elementSize = computed<ElementSizeType>(() => ({
    visible: !!resizing.value && resizing.value.state === 'resizing',
    position: elementPosition.value,
    size: resizing.value ? resizing.value.size : 0
  }))

  const getSize = (dimension: K): number => {
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
    elementSize,
    getSize,
    mousemove,
    mouseleave,
    mousedown,
    mouseup
  }
}
