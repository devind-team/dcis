import { ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'

export type RangeType = string

/**
 * Режим работы таблицы
 * CHANGE - пользователь может менять структуру документа
 * WRITE - пользователь может вносить данные, изменяя модель Value
 * READ - документ доступен только для чтения
 */
export enum GridMode {
  CHANGE,
  WRITE,
  READ
}

/**
 * Кодовые ошибки
 */
export enum ErrorCode {
  NULL= '#NULL!',
  DIV = '#DIV/0!',
  VALUE = '#VALUE!',
  REF = '#REF!',
  NAME = '#NAME!',
  NUM = '#NUM!',
  NA = '#N/A!'
}

/**
 * Метод агрегации расширяемых столбцов
 */
export enum AggregationMethod {
  MAX,
  MIN,
  SUM,
  AVG,
}

export type PositionPartsType = {
  column: string,
  row: number
}

export type SheetPositionPartsType = PositionPartsType & {
  sheet: string
}

export type RangePartsType = {
  minColumn: string
  minRow: number
  maxColumn: string
  maxRow: number
}

export type SheetRangePartsType = RangePartsType & {
  sheet: string
}

export type RangeIndicesType = {
  minColumn: number
  minRow: number
  maxColumn: number
  maxRow: number
}

export type RangeSpanType = {
  target: RangeType
  colspan: number
  rowspan: number
  cells: string[]
}

export type MousePositionType = {
  x: number
  y: number
}

export type ElementPositionType = {
  left: number | null
  right: number | null
  top: number | null
  bottom: number | null
}

export type GlobalSelectionType = {
  visible: boolean
  position: ElementPositionType
  zIndex: number
  width: number
  height: number
}

export type ElementResizingType = {
  visible: boolean
  position: ElementPositionType
  size: number
}

export type ResizingType<T> = {
  object: T
  size: number
  mousePosition: MousePositionType
  state: 'hover' | 'resizing'
}

export type BuildCellType = {
  style: Record<string, string>
  columnDimension: ColumnDimensionType
  rowDimension: RowDimensionType
  cell: CellType
}

export type BuildColumnType = {
  columnDimension: ColumnDimensionType
}

export type BuildRowType = {
  rowDimension: RowDimensionType
  buildCells: BuildCellType[]
}

export type Selection<T> = {
  first: T,
  last: T,
}

export type CellOptionsType = {
  kind: string | null,
  horizontalAlign: 'left' | 'center' | 'right' | null
  verticalAlign: 'top' | 'middle' | 'bottom' | null
  size: number | null
  strong: boolean | null
  italic: boolean | null
  strike: boolean | null
  underline: string | null
}

/**
 * Ячейка граничная к крайнему фиксированному столбцу
 */
export type BoundaryColumnCell = {
  buildCell: BuildCellType,
  buildRows: BuildRowType[],
}

/**
 * Ячейка граничная к крайней фиксированной строке
 */
export type BoundaryRowCell = {
  buildCell: BuildCellType
  buildColumns: BuildColumnType[]
}
