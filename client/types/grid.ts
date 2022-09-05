import {
  CellType,
  ColumnDimensionType,
  RowDimensionType,
  DocumentSheetQuery,
  DocumentsSheetQuery
} from '~/types/graphql'
import { UpdateType } from '~/composables'

export type RangeType = string

/**
 * Режим работы таблицы
 * CHANGE - пользователь может менять структуру документа
 * WRITE - пользователь может вносить данные, изменяя модель Value
 */
export enum GridMode {
  CHANGE,
  WRITE
}

export type UpdateSheetType = UpdateType<DocumentsSheetQuery | DocumentSheetQuery>

/*
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

export type SelectionType<T> = {
  first: T,
  last: T,
}

export type SelectionViewType = {
  id: string
  position: ElementPositionType
  width: number
  height: number
  border: {
    top: boolean
    right: boolean
    bottom: boolean
    left: boolean
  }
}

export type ScrollInfoType = {
  left: number
  top: number
  width: number
  height: number
}

export type FixedInfoType = {
  fixed: boolean,
  position: number | null
}

export type CellsOptionsType = {
  cells: CellType[]
  strong: boolean | null
  italic: boolean | null
  strike: boolean | null
  underline: string | null
  horizontalAlign: 'left' | 'center' | 'right' | null
  verticalAlign: 'top' | 'middle' | 'bottom' | null
  editable: boolean
  size: number | null
  kind: string | null
}

export type ColumnDimensionsOptionsType = {
  columnDimensions: ColumnDimensionType[]
  fixed: boolean
  rectangular: boolean
}

export type RowDimensionsOptionsType = {
  rowDimensions: RowDimensionType[]
  fixed: boolean
  rectangular: boolean
}
