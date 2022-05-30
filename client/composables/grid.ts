import { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'

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
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => Promise<void>,
  changeRowHeight: (rowDimension: RowDimensionType, height: number) => Promise<void>
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
    cellsSelectionView,
    rowsSelectionView,
    columnsSelectionView,
    boundarySelectedColumnsPositions,
    boundarySelectedRowsPositions,
    allCellsSelected,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
    updateSelectionViews,
    clearSelection,
    selectAllCells,
    gridContainerScroll,
    mousedownCell,
    mouseenterCell,
    mouseupCell,
    mouseenterColumnName,
    mouseDownColumnName: mouseDownColumnNameSelection,
    mouseenterRowName,
    mousedownRowName: mouseDownRowNameSelection
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
  watch(resizingColumnWidth, () => updateSelectionViews(), { deep: true })
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
  watch(resizingRowHeight, () => updateSelectionViews(), { deep: true })

  const gridWidth = computed<number>(
    () => rowNameColumnWidth.value +
      sheet.value.columns.reduce((sum: number, column: ColumnDimensionType) => sum + getColumnWidth(column), 0)
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
  const mouseupColumnName = async () => {
    await mouseupColumnNameResizing()
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
  const mouseupRowName = async () => {
    await mouseupRowNameResizing()
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
    cellsSelectionView,
    rowsSelectionView,
    columnsSelectionView,
    boundarySelectedColumnsPositions,
    boundarySelectedRowsPositions,
    allCellsSelected,
    selectedColumnsPositions,
    selectedRowsPositions,
    selectedCellsOptions,
    clearSelection,
    selectAllCells,
    gridContainerScroll,
    mousedownCell,
    mouseenterCell,
    mouseupCell,
    mouseenterColumnName,
    mousemoveColumnName,
    mouseleaveColumnName,
    mousedownColumnName,
    mouseupColumnName,
    mouseenterRowName,
    mousemoveRowName,
    mouseleaveRowName,
    mousedownRowName,
    mouseupRowName
  }
}
