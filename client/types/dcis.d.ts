import type { UserType } from '~/types/graphql'

export type CellPositionType = string
export type RangeType = string

export type AlignTextType = 'JUSTIFY' | 'LEFT' | 'CENTER' | 'RIGHT'
export type CellOptionsType = {
  align: AlignTextType
  bold: boolean
  italic: boolean
  color?: string
  background?: string
}
export type CellKindType = 'STRING' | 'FORMULA' | 'NUMERIC' | 'BOOL' | 'NULL' | 'INLINE' | 'ERROR'
export type CellType = {
  id: string
  kind: CellKindType
  options: CellOptionsType
  formula?: string
  value?: string
  info?: string
}

export type MergeCellType = {
  colspan: number
  rowspan: number
  cells: CellPositionType[]
}
export type MergeCellsType = {
  [cell: RangeType]: MergeCellType
}

export type BuildCellType = {
  columnIndex: number
  position: CellPositionType
  colspan: number
  rowspan: number
  originCell: CellType
}

export type ColumnDimensionType = {
  id: string
  index: number
  width: number
  hidden: boolean
  collapsed: boolean
}
export type ColumnsDimensionType = Record<number, ColumnDimensionType>

export type RowDimensionType = {
  id: string
  index: number
  height: number
  hidden: boolean
  collapsed: boolean
}
export type RowsDimensionType = Record<number, RowDimensionType>

export type BuildColumnType = {
  name: string
  style: Record<string, string>
}

export type RowType = {
  cells: CellType[]
  user: UserType
}

export type BuildRowType = {
  rowIndex: number
  buildCells: BuildCellType[]
  style: Record<string, string>
  originRow: RowType
}

export type SheetType = {
  id: string
  name: string
  columnsCount: number
  columnsDimension: ColumnsDimensionType
  rowsCount: number
  rowsDimension: RowsDimensionType
  rows: RowType[]
  mergeCells: MergeCellsType
}
export type DocumentUserType = {
  id: string
  user: UserType
  active: boolean
  color: string
}
export type DocumentType = {
  id: string
  name: string
  users: DocumentUserType[]
  sheets: SheetType[]
}
