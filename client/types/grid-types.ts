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
export enum  ErrorCode {
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
  minColumn: number,
  minRow: number,
  maxColumn: number,
  maxRow: number
}

/**
 * Опции ячейки
 */

export type CellOptionValueType = string | boolean | null


export type CellOptionsType = {
  align: AlignText
  bold: boolean
  italic: boolean
  color?: string
  background?: string
}
/**
 * Описание значений ячейки
 */
export type CellType = {
  uid: string
  kind: KindCell
  options: CellOptionsType
  formula?: string
  value?: string
  info?: string
}

/**
 * Тип ячейки
 * cells - набор ячеек
 * dynamic - динмическа ли ячейка
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
 *   rowspan - объединение по строка
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

/**
 * Callback функции на события
 *   changeCellValue - изменение значения ячейки
 *   changeCllOption - изменение опции ячейки
 */
export type CallbacksType = {
  changeCellValue?: (
    column: number,
    row: number,
    newValue: string,
    oldValue?: string) => void
  changeCellOption?: (
    column: number,
    row: number,
    option: string,
    newValue: CellOptionValueType,
    oldValue?: CellOptionValueType) => void
}

/**
 * Описание информации о колонках
 */
export type ColumnDimensionType = {
  index: string
  width: number
  min: number
  max: number
  hidden: boolean
  collapsed: boolean
  autoSize: boolean
  color?: string
  background?: string
}

export type ColumnsDimensionType = {
  [index: string]: ColumnDimensionType
}

/**
 * Описание информации о строках
 */
export type RowDimensionType = {
  index: number
  height: number
  hidden: boolean
  collapse?: boolean
  color?: string
}

export type RowsDimensionType = {
  [index: number]: RowDimensionType
}

/**
 * Описание типа сетки документа
 */
export type GridType = {
  name: string
  columnsCount: number
  columnsDimension: ColumnsDimensionType
  rowsCount: number
  rowsDimension: RowsDimensionType
  rows: RowType[]
  mergedCells: MergeCellsType,
  mode: GridMode
}

export type MergedType = {
  merged: boolean
  unmerged: boolean
}
