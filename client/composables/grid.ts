import { useEventListener } from '@vueuse/core'
import type { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  ElementPositionType,
  BuildCellType,
  BuildColumnType,
  ResizingBuildColumnType,
  ColumnWidthType,
  BuildRowType,
  ResizingBuildRowType,
  RowHeightType,
  CellOptionsType,
  BoundaryColumnCell,
  BoundaryRowCell, RangeIndicesType
} from '~/types/grid'
import {
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
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => void
) {
  const rowIndexColumnWidth = ref<number>(30)
  const defaultColumnWidth = ref<number>(64)
  const borderGag = ref<number>(10)

  const resizingColumn = ref<ResizingBuildColumnType | null>(null)
  const columnWidthPosition = ref<ElementPositionType>({ left: null, right: null, top: null, bottom: null })
  const columnWidth = computed<ColumnWidthType>(() => ({
    visible: !!resizingColumn.value && resizingColumn.value.state === 'resizing',
    position: columnWidthPosition.value,
    width: resizingColumn.value?.width ?? 0
  }))

  const resizingRow = ref<ResizingBuildRowType | null>(null)
  const rowHeightPosition = ref<ElementPositionType>({ left: null, right: null, top: null, bottom: null })
  const rowHeight = computed<RowHeightType>(() => ({
    visible: !!resizingRow.value && resizingRow.value.state === 'resizing',
    position: rowHeightPosition.value,
    height: resizingRow.value?.height ?? 0
  }))

  /**
   * Структура для быстрого поиска колонок
   */
  const columnsMap = computed<Record<string, ColumnDimensionType>>(() =>
    sheet.value.columns.reduce((a, c: ColumnDimensionType) => ({ ...a, [c.id]: c }), {})
  )

  const rows = computed<BuildRowType[]>(() =>
    sheet.value.rows.map((rowDimension: RowDimensionType) => {
      let height = 0
      if (resizingRow.value && resizingRow.value.buildRow.rowDimension.id === rowDimension.id) {
        height = resizingRow.value.height
      } else {
        height = rowDimension.height ?? null
      }
      return {
        style: { height: height ? `${height}px` : undefined },
        height,
        rowDimension,
        buildCells: rowDimension.cells.map((cell: CellType) => {
          return {
            style: getCellStyle(cell),
            columnDimension: columnsMap.value[cell.columnId],
            rowDimension,
            cell
          }
        })
      }
    })
  )

  const columns = computed<BuildColumnType[]>(() =>
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => {
      let width = 0
      if (resizingColumn.value && resizingColumn.value.buildColumn.columnDimension.id === columnDimension.id) {
        width = resizingColumn.value.width
      } else {
        width = columnDimension.width ? columnDimension.width : defaultColumnWidth.value
      }
      return {
        style: { width: `${width}px` },
        width,
        columnDimension,
        buildCells: rows.value
          .map((buildRow: BuildRowType) => buildRow.buildCells.find(
            (buildCell: BuildCellType) => buildCell.columnDimension.id === columnDimension.id)
          )
          .filter((buildCell: BuildCellType | undefined) => buildCell)
      }
    })
  )

  const gridContainer = ref<HTMLDivElement | null>(null)

  const gridWidth = computed<number>(
    () => rowIndexColumnWidth.value +
      columns.value.reduce((sum, column) => sum + column.width, 0)
  )

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

  const mouseenterColumnIndex = (buildColumn: BuildColumnType) => {
    if (selectionState.value === 'column') {
      selection.value.last = buildColumn.buildCells.at(-1)
    }
  }
  const mousemoveColumnIndex = (buildColumn: BuildColumnType, event: MouseEvent) => {
    const mousePosition = { x: event.clientX, y: event.clientY }
    const cell = event.target as HTMLTableCellElement
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      resizingColumn.value.width = Math.max(
        resizingColumn.value.width + mousePosition.x - resizingColumn.value.mousePosition.x, 0
      )
      resizingColumn.value.mousePosition = mousePosition
    } else if (cell.offsetWidth - event.offsetX < borderGag.value) {
      resizingColumn.value = {
        buildColumn,
        width: buildColumn.columnDimension.width ?? defaultColumnWidth.value,
        mousePosition,
        state: 'hover'
      }
    } else if (
      cell.offsetWidth - event.offsetX > cell.offsetWidth - borderGag.value &&
      buildColumn.columnDimension.index - 1 > 0
    ) {
      resizingColumn.value = {
        buildColumn: columns.value[buildColumn.columnDimension.index - 2],
        width: columns.value[buildColumn.columnDimension.index - 2].columnDimension.width ?? defaultColumnWidth.value,
        mousePosition,
        state: 'hover'
      }
    } else {
      resizingColumn.value = null
    }
  }
  const mouseleaveColumnIndex = () => {
    if (resizingColumn.value && resizingColumn.value.state === 'hover') {
      resizingColumn.value = null
    }
  }
  const mousedownColumnIndex = (buildColumn: BuildColumnType, event: MouseEvent) => {
    if (resizingColumn.value) {
      const cell = event.target as HTMLTableCellElement
      if (cell.offsetLeft - gridContainer.value.scrollLeft + event.offsetX < document.body.offsetWidth - 150) {
        columnWidthPosition.value = {
          left: cell.offsetLeft - gridContainer.value.scrollLeft + event.offsetX,
          right: null,
          top: cell.offsetTop + event.offsetY - 25,
          bottom: null
        }
      } else {
        columnWidthPosition.value = {
          left: null,
          right: 25,
          top: cell.offsetTop + event.offsetY - 25,
          bottom: null
        }
      }
      resizingColumn.value.state = 'resizing'
    } else {
      selectionState.value = 'column'
      selection.value = {
        first: buildColumn.buildCells[0],
        last: buildColumn.buildCells.at(-1)
      }
    }
  }
  const mouseupColumnIndex = () => {
    if (resizingColumn.value) {
      changeColumnWidth(resizingColumn.value.buildColumn.columnDimension, resizingColumn.value.width)
      resizingColumn.value.state = 'hover'
    }
  }

  const mouseenterRowIndex = (buildRow: BuildRowType) => {
    if (selectionState.value === 'row') {
      selection.value.last = buildRow.buildCells.at(-1)
    }
  }
  const mousedownRowIndex = (buildRow: BuildRowType) => {
    selectionState.value = 'row'
    selection.value = {
      first: buildRow.buildCells[0],
      last: buildRow.buildCells.at(-1)
    }
  }

  const selectAllCells = () => {
    selection.value = {
      first: rows.value[0].buildCells[0],
      last: rows.value.at(-1).buildCells.at(-1)
    }
  }

  /**
   * Класс курсора на странице
   */
  const cursorClass = computed<'grid__cursor_cell' | 'grid__cursor_col-resize' | null>(() => {
    if (selectionState.value) {
      return 'grid__cursor_cell'
    }
    if (resizingColumn.value) {
      return 'grid__cursor_col-resize'
    }
    return null
  })
  useOverlyingClass(document.body, cursorClass)

  useEventListener('mouseup', () => {
    if (selectionState.value) {
      selectionState.value = null
    }
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      changeColumnWidth(resizingColumn.value.buildColumn.columnDimension, resizingColumn.value.width)
      resizingColumn.value = null
    }
  })

  useEventListener('mousemove', (event: MouseEvent) => {
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      const mousePosition = { x: event.clientX, y: event.clientY }
      resizingColumn.value.width = Math.max(
        resizingColumn.value.width + mousePosition.x - resizingColumn.value.mousePosition.x, 0
      )
      resizingColumn.value.mousePosition = mousePosition
    }
  })

  return {
    rowIndexColumnWidth,
    columnWidth,
    rowHeight,
    rows,
    columns,
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
    mouseenterColumnIndex,
    mousemoveColumnIndex,
    mouseleaveColumnIndex,
    mousedownColumnIndex,
    mouseupColumnIndex,
    mouseenterRowIndex,
    mousedownRowIndex,
    selectAllCells
  }
}
