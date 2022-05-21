import { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'
import {
  ElementResizingType,
  BoundaryColumnCell,
  BoundaryRowCell
} from '~/types/grid'

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

  const activeCell = ref<CellType | null>(null)
  const setActiveCell = (cell: CellType | null) => {
    activeCell.value = cell
  }

  const {
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
    mouseDownColumnName: mouseDownColumnNameSelection,
    mouseenterRowName,
    mousedownRowName: mouseDownRowNameSelection,
    selectAllCells
  } = useGridSelection(sheet, gridContainer, grid, setActiveCell)

  const {
    resizing: resizingColumn,
    elementResizing: resizingColumnWidth,
    getSize: getColumnWidth,
    mousemove: mousemoveColumnNameResizing,
    mouseleave: mouseleaveColumnNameResizing,
    mousedown: mousedownColumnNameResizing,
    mouseup: mouseupColumnNameResizing
  } = useGridResizing<ColumnDimensionType>(
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
  } = useGridResizing<RowDimensionType>(
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
      mouseDownColumnNameSelection(column)
    }
  }
  const mouseupColumnName = () => {
    mouseupColumnNameResizing()
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
      mouseDownRowNameSelection(row)
    }
  }
  const mouseupRowName = () => {
    mouseupRowNameResizing()
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
