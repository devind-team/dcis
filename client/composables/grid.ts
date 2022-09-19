import { useEventListener } from '@vueuse/core'
import { computed, ref, Ref } from '#app'
import { CellType, ColumnDimensionType, RowDimensionType, SheetType } from '~/types/graphql'
import { useGridResizing } from '~/composables/grid-resizing'
import { GridMode, ScrollInfoType, FixedInfoType, RowFixedInfoType } from '~/types/grid'
import { letterToPosition, parsePosition, positionsToRangeIndices } from '~/services/grid'

export const cellKinds = {
  n: 'Numeric',
  s: 'String',
  f: 'Formula',
  text: 'Text',
  fl: 'Files',
  money: 'Money',
  department: 'Department',
  classification: 'Classification'
}

export function useGrid (
  mode: GridMode,
  sheet: Ref<SheetType>,
  gridContainer: Ref<HTMLDivElement | null>,
  grid: Ref<HTMLTableElement | null>,
  canChangeRowHeight: (rowDimension: RowDimensionType) => boolean,
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => Promise<void> | null,
  changeRowHeight: (rowDimension: RowDimensionType, height: number) => Promise<void>
) {
  /**
   * Ширина первого столбца
   */
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
    return maxDigits * 12 + maxDots * 2 + 10
  })
  /**
   * Высота первой строки
   */
  const columnNameRowHeight = 25

  const gridWidth = computed<number>(
    () => rowNameColumnWidth.value +
      sheet.value.columns.reduce((sum: number, column: ColumnDimensionType) => sum + getColumnWidth(column), 0)
  )

  const activeCell = ref<CellType | null>(null)
  const setActiveCell = (cell: CellType | null) => {
    activeCell.value = cell
  }

  const scroll = ref<ScrollInfoType>({
    left: 0,
    top: 0,
    height: 0,
    width: 0
  })
  const updateScroll = () => {
    scroll.value.left = gridContainer.value.scrollLeft
    scroll.value.top = gridContainer.value.scrollTop
    scroll.value.height = gridContainer.value.scrollHeight
    scroll.value.width = gridContainer.value.scrollWidth
  }
  useEventListener(gridContainer, 'scroll', updateScroll)

  const {
    resizing: resizingColumn,
    elementResizing: resizingColumnWidth,
    getSize: getColumnWidth,
    mousemove: mousemoveColumnNameResizing,
    mouseleave: mouseleaveColumnNameResizing,
    mousedown: mousedownColumnNameResizing,
    mouseup: mouseupColumnNameResizing
  } = useGridResizing<ColumnDimensionType>(
    scroll,
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
    scroll,
    25,
    'y',
    changeRowHeight
  )
  watch(resizingRowHeight, () => updateSelectionViews(), { deep: true })

  const fixedColumns = computed<ColumnDimensionType[]>(() =>
    sheet.value.columns.filter((columnDimension: ColumnDimensionType) => columnDimension.fixed))
  const fixedRows = computed<RowDimensionType[]>(() =>
    sheet.value.rows.filter((rowDimension: RowDimensionType) => rowDimension.fixed))
  const fixedRowsIndex = computed<Record<string, number>>(() =>
    fixedRows.value.reduce((acc: Record<string, number>, row: RowDimensionType, index: number) => ({
      ...acc, [row.id]: index
    }), {}))
  const fixedColumnsLeft = computed<Record<string, number>>(() => {
    let width = rowNameColumnWidth.value
    const result = {}
    for (const fixedColumn of fixedColumns.value) {
      result[fixedColumn.id] = width
      width += getColumnWidth(fixedColumn)
    }
    return result
  })
  const fixedRowsTop = computed<Record<string, number>>(() => {
    let height = columnNameRowHeight
    const result = {}
    for (const fixedRow of fixedRows.value) {
      result[fixedRow.id] = height
      height += getRowHeight(fixedRow) + 1
    }
    return result
  })
  const getColumnFixedInfo = (column: ColumnDimensionType): FixedInfoType => {
    if (column.fixed) {
      return { fixed: true, position: fixedColumnsLeft.value[column.id] }
    }
    return { fixed: false, position: null }
  }
  const getRowFixedInfo = (row: RowDimensionType): RowFixedInfoType => {
    if (row.fixed) {
      return {
        fixed: true,
        position: fixedRowsTop.value[row.id],
        reverseIndex: fixedRows.value.length - fixedRowsIndex.value[row.id]
      }
    }
    return { fixed: false, position: null, reverseIndex: null }
  }
  const getCellFixedInfo = (cell: CellType): FixedInfoType => {
    const column = sheet.value.columns[letterToPosition(parsePosition(cell.globalPosition).column) - 1]
    return getColumnFixedInfo(column)
  }

  const borderFixedColumn = computed<ColumnDimensionType | null>(() => {
    let width = 0
    let fixedWidth = 0
    let borderColumn: ColumnDimensionType | null = null
    for (const column of sheet.value.columns) {
      if (column.fixed && scroll.value.left > width - fixedWidth) {
        fixedWidth += getColumnWidth(column)
        borderColumn = column
      }
      width += getColumnWidth(column)
    }
    return borderColumn
  })
  const borderFixedRow = computed<RowDimensionType | null>(() => {
    let height = 0
    let fixedHeight = 0
    let borderRow: RowDimensionType | null = null
    for (const row of sheet.value.rows) {
      if (row.fixed && scroll.value.top > height - fixedHeight) {
        fixedHeight += getRowHeight(row) + 1
        borderRow = row
      }
      height += getRowHeight(row) + 1
    }
    return borderRow
  })
  const isColumnFixedBorder = (column: ColumnDimensionType): boolean => {
    if (!borderFixedColumn.value) {
      return false
    }
    return borderFixedColumn.value.id === column.id
  }
  const isRowFixedBorder = (row: RowDimensionType): boolean => {
    if (!borderFixedRow.value) {
      return false
    }
    return borderFixedRow.value.id === row.id
  }
  const isCellFixedBorderRight = (cell: CellType): boolean => {
    return isColumnFixedBorder(sheet.value.columns[positionsToRangeIndices(cell.relatedGlobalPositions).maxColumn - 1])
  }
  const isCellFixedBorderBottom = (cell: CellType): boolean => {
    return isRowFixedBorder(sheet.value.rows[positionsToRangeIndices(cell.relatedGlobalPositions).maxRow - 1])
  }

  const {
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
    mouseDownColumnName: mouseDownColumnNameSelection,
    mouseenterRowName,
    mousedownRowName: mouseDownRowNameSelection
  } = useGridSelection(
    sheet,
    scroll,
    grid,
    setActiveCell
  )

  const mousemoveColumnName = (column: ColumnDimensionType, event: MouseEvent) => {
    if (mode === GridMode.CHANGE) {
      mousemoveColumnNameResizing(
        column,
        column.index - 1 > 0
          ? sheet.value.columns[column.index - 2]
          : null,
        event,
        (_: ColumnDimensionType) => true
      )
    }
  }
  const mouseleaveColumnName = () => {
    mouseleaveColumnNameResizing()
  }
  const mousedownColumnName = (column: ColumnDimensionType, event: MouseEvent) => {
    if (resizingColumn.value) {
      mousedownColumnNameResizing(event)
    } else if (mode === GridMode.CHANGE) {
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
      event,
      canChangeRowHeight
    )
  }
  const mouseleaveRowName = () => {
    mouseleaveRowNameResizing()
  }
  const mousedownRowName = (row: RowDimensionType, event: MouseEvent) => {
    if (resizingRow.value) {
      mousedownRowNameResizing(event)
    } else if (mode === GridMode.CHANGE) {
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
  onMounted(() => {
    updateScroll()
    useOverlyingClass(document.body, cursorClass)
  })

  return {
    rowNameColumnWidth,
    columnNameRowHeight,
    gridWidth,
    activeCell,
    setActiveCell,
    resizingColumn,
    resizingColumnWidth,
    getColumnWidth,
    resizingRow,
    resizingRowHeight,
    getRowHeight,
    getColumnFixedInfo,
    getRowFixedInfo,
    getCellFixedInfo,
    borderFixedColumn,
    borderFixedRow,
    isColumnFixedBorder,
    isRowFixedBorder,
    isCellFixedBorderRight,
    isCellFixedBorderBottom,
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
    clearSelection,
    selectAllCells,
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
