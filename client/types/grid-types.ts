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

export type RangeSpanType = {
  target: RangeType
  colspan: number
  rowspan: number
  cells: CellPositionType[]
}
