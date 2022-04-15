import type { ColumnDimensionType, RowDimensionType, CellType } from '~/types/graphql'

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

export type BuildColumnType = {
  id: string
  index: number
  position: string
  width: number
  style: Record<string, string | undefined>
  dimension: ColumnDimensionType
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

export type BuildCellType = {
  sheetId: string
  id: string
  position: string
  value: string
  editable: boolean
  kind: string
  colspan: number
  rowspan: number
  style: Record<string, number | string | undefined> | string,
  border: Record<string, string | undefined | null> | string
  cell: CellType
}

export type BuildRowType = {
  sheetId: string
  id: string
  index: number
  dynamic: boolean
  style: Record<string, string | undefined>
  cells: BuildCellType[],
  dimension: RowDimensionType
}

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

/**
 * Режимы работы таблицы
 *   edit - режим редактирования таблицы
 *   write - режим заполнения таблицы
 *   readonly - режим просмотра таблицы
 */

export enum GridMode {
  EDIT,
  WRITE,
  READONLY
}

/**
 * Выравнивание текста
 */
export enum AlignText {
  JUSTIFY = 'justify',
  LEFT = 'left',
  CENTER = 'center',
  RIGHT = 'right'
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

/**
 * Типы ячейки
 */
export enum KindCell {
  STRING = 's',
  FORMULA = 'f',
  NUMERIC = 'n',
  BOOl = 'b',
  NULL = 'n',
  INLINE = 'inlineStr',
  ERROR = 'e'
}

export type CellPositionType = string
export type RangeType = string

export type RangePositionsType = {
  minColumn: number
  minRow: number
  maxColumn: number
  maxRow: number
}

/**
 * Опции ячейки
 */

export type CellOptionValueType = string | boolean | null

export type CellOptionsType = {
  kind: string | null,
  horizontalAlign: 'left' | 'center' | 'right' | null
  verticalAlign: 'top' | 'middle' | 'bottom' | null
  size: number | null
  strong: boolean | null
  italic: boolean | null
  underline: boolean | null
}

/**
 * Тип ячейки
 * cells - набор ячеек
 * dynamic - динамическая ли ячейка
 * aggregation - набор агрегаций для колонок
 */
export type RowType = {
  cells: CellType[]
  dynamic: boolean
  fixed: boolean
  filter: boolean
  height?: number
  aggregation?: {
    [column: string]: AggregationMethod
  },
  children?: RowType[]
}

/**
 * cell - позиция ячейки формата A1, B2, C10 ...
 *   colspan - объединение по столбцам
 *   rowspan - объединение по строкам
 *   cells - объединенные ячейки (значения объединенных ячеек всегда null)
 */
export type MergeCellType = {
  colspan: number
  rowspan: number
  cells: CellPositionType[]
}

/**
 * Тип ячейки при выводе
 *   columnIndex - позиция колонки
 *   position - позиция ячейки A1
 */
export type MergeBuildCellType = CellType & {
  columnIndex: number
  position: string
  colspan: number
  rowspan: number
  originCell: CellType
}

/**
 * Тип смердженной ячейки
 *   buildCells - содержит ячейки для отображения
 *   rowIndex - индекс таблицы
 */
export type MergeRowType = RowType & {
  buildCells: MergeBuildCellType[]
  rowIndex: number
}

export type MergeCellsType = {
  [cell: RangeType]: MergeCellType
}

export type RangeSpanType = {
  target: RangeType
  colspan: number
  rowspan: number
  cells: CellPositionType[]
}

export type StyleCellType = {
  [cell: RangeType]: string
}

export type SheetType = MergeRowType[]

export type MergedType = {
  merged: boolean
  unmerged: boolean
}
