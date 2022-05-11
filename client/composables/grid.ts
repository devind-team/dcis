import type { Ref } from '#app'
import { SheetType, ColumnDimensionType, RowDimensionType, CellType, MergedCellType } from '~/types/graphql'
import {
  BuildColumnType,
  ResizingBuildColumnType,
  BuildRowType,
  ResizingBuildRowType, BuildCellType
} from '~/types/grid'
import { positionToLetter, rangeToCellPositions, getCellStyle } from '~/services/grid'

export const cellKinds = {
  n: 'Numeric',
  s: 'String',
  text: 'Text',
  fl: 'Files',
  money: 'Money',
  department: 'Department',
  classification: 'Classification'
}

export function useGrid (sheet: Ref<SheetType>) {
  const rowIndexColumnWidth = ref<number>(30)
  const defaultColumnWidth = ref<number>(64)
  const borderGag = ref<number>(10)

  const resizingColumn = ref<ResizingBuildColumnType | null>(null)
  const resizingRow = ref<ResizingBuildRowType | null>(null)

  /**
   * Структура для быстрого поиска колонок
   */
  const columnsRecord = computed<Record<string, ColumnDimensionType>>(() =>
    sheet.value.columns.reduce((a, c: ColumnDimensionType) => ({ ...a, [c.id]: c }), {})
  )

  /**
   * Структура для быстрого поиска объединенных ячеек
   */
  const mergedCellsRecord = computed<Record<string, MergedCellType>>(() =>
    sheet.value.mergedCells.reduce((a, c: MergedCellType) => ({ ...a, [c.target]: c }), {})
  )

  /**
   * Все объединенные ячейки
   */
  const mergedCells = computed<string[]>(() => {
    return Object.values<MergedCellType>(sheet.value.mergedCells)
      .reduce<string[]>((a: string[], c: MergedCellType) => ([...a, ...c.cells]), [])
  })

  const columns = computed<BuildColumnType[]>(() =>
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => {
      let width = 0
      if (resizingColumn.value && resizingColumn.value.columnDimension.id === columnDimension.id) {
        width = resizingColumn.value.width
      } else {
        width = columnDimension.width ? columnDimension.width : defaultColumnWidth.value
      }
      return {
        style: { width: `${width}px` },
        width,
        columnDimension
      }
    })
  )

  const rows = computed<BuildRowType[]>(() =>
    sheet.value.rows.map((rowDimension: RowDimensionType) => {
      let height = 0
      if (resizingRow.value && resizingRow.value.rowDimension.id === rowDimension.id) {
        height = resizingRow.value.height
      } else {
        height = rowDimension.height ?? null
      }
      const buildCells = rowDimension.cells.map((cell: CellType) => {
        const columnDimension = columnsRecord.value[cell.columnId]
        const letter = positionToLetter(columnDimension.index)
        const position = `${letter}${rowDimension.index}`
        const mergedCell = position in mergedCellsRecord.value ? mergedCellsRecord.value[position] : null
        return {
          position,
          globalPosition: `${letter}${rowDimension.globalIndex}`,
          colspan: mergedCell ? mergedCell.colspan : 1,
          rowspan: mergedCell ? mergedCell.rowspan : 1,
          style: getCellStyle(cell),
          columnDimension,
          rowDimension,
          cell
        }
      })
      return {
        style: { height: height ? `${height}px` : undefined },
        height,
        rowDimension,
        cells: buildCells.filter((buildCell: BuildCellType) =>
          buildCell.position in mergedCellsRecord.value || !mergedCells.value.includes(buildCell.position)
        )
      }
    })
  )

  const gridContainer = ref<HTMLDivElement | null>(null)

  const gridWidth = computed<number>(
    () => rowIndexColumnWidth.value +
      columns.value.reduce((sum, column) => sum + column.width, 0)
  )

  const activeCell = ref<BuildCellType | null>(null)
  const firstSelectedCell = ref<BuildCellType | null>(null)
  const lastSelectedCell = ref<BuildCellType | null>(null)
  const allCellsRange = computed<string>(() =>
    `A1:${columns.value.at(-1).columnDimension.index}${rows.value.at(-1).rowDimension.globalIndex}`)
  const selectedCellsRange = computed<string | null>(() => {
    if (firstSelectedCell.value && lastSelectedCell.value) {
      return `${firstSelectedCell.value.globalPosition}:${lastSelectedCell.value.globalPosition}`
    } else if (firstSelectedCell.value) {
      return `${firstSelectedCell.value.globalPosition}:${firstSelectedCell.value.globalPosition}`
    }
    return null
  })
  const selectedCellPositions = computed<string[]>(() => {
    if (selectedCellsRange.value) {
      return rangeToCellPositions(selectedCellsRange.value)
    }
    return []
  })
  const selectedColumnPositions = computed<number[]>(() => {
    if (firstSelectedCell.value && lastSelectedCell.value) {
      return Array.from({
        length: lastSelectedCell.value.columnDimension.index - firstSelectedCell.value.columnDimension.index + 1
      }).map((_, i) => i + firstSelectedCell.value.columnDimension.index)
    } else if (firstSelectedCell.value) {
      return [firstSelectedCell.value.columnDimension.index]
    }
    return []
  })
  const selectedRowPositions = computed<number[]>(() => {
    if (firstSelectedCell.value && lastSelectedCell.value) {
      return Array.from({
        length: lastSelectedCell.value.rowDimension.globalIndex - firstSelectedCell.value.rowDimension.globalIndex
      }).map((_, i) => i + firstSelectedCell.value.rowDimension.globalIndex)
    } else if (firstSelectedCell.value) {
      return [firstSelectedCell.value.rowDimension.globalIndex]
    }
    return []
  })
  const allCellsSelected = computed<boolean>(() => selectedCellsRange.value === allCellsRange.value)

  const mousedownCell = (buildCell: BuildCellType): void => {
    firstSelectedCell.value = buildCell
    lastSelectedCell.value = null
  }

  const mouseenterCell = (buildCell: BuildCellType): void => {
    if (firstSelectedCell.value && buildCell.cell.id !== firstSelectedCell.value.cell.id) {
      lastSelectedCell.value = buildCell
    }
  }

  const mouseupCell = (buildCell: BuildCellType): void => {
    if (firstSelectedCell.value && lastSelectedCell.value) {
      activeCell.value = buildCell
    }
  }

  return {
    rowIndexColumnWidth,
    rows,
    columns,
    gridContainer,
    gridWidth,
    activeCell,
    selectedCellPositions,
    selectedColumnPositions,
    selectedRowPositions,
    allCellsSelected,
    mousedownCell,
    mouseenterCell,
    mouseupCell
  }
}
