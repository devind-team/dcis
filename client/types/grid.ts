import { ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'

export type MousePositionType = {
  x: number
  y: number
}

export type PositionType = {
  left: number | null
  right: number | null
  top: number | null
  bottom: number | null
}

export type BuildCellType = {
  position: string
  globalPosition: string
  colspan: number
  rowspan: number
  style: Record<string, string>
  columnDimension: ColumnDimensionType
  rowDimension: RowDimensionType
  cell: CellType
}

export type BuildColumnType = {
  style: Record<string, string>
  width: number
  columnDimension: ColumnDimensionType
}

export type ResizingBuildColumnType = {
  width: number
  mousePosition: MousePositionType
  state: 'hover' | 'resizing'
} & BuildColumnType

export type ColumnWidthType = {
  visible: boolean
  position: PositionType
  width: number
}

export type BuildRowType = {
  style: Record<string, string>
  height: number | null
  rowDimension: RowDimensionType
  cells: BuildCellType[]
}

export type ResizingBuildRowType = {
  height: number
  mousePosition: MousePositionType
  state: 'hover' | 'resizing'
} & BuildRowType

/**
 * Ячейка граничная к крайнему фиксированному столбцу
 */
export type BoundaryColumnCell = {
  cell: BuildCellType,
  rows: BuildRowType[],
}

/**
 * Ячейка граничная к крайней фиксированной строке
 */
export type BoundaryRowCell = {
  cell: BuildCellType
  columns: BuildColumnType[]
}
