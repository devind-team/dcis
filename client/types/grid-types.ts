import type { CellType } from '~/types/graphql'

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
