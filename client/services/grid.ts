import { SheetType, CellType, RowDimensionType, ColumnDimensionType } from '~/types/graphql'
import {
  RangeType,
  PositionPartsType,
  SheetPositionPartsType,
  RangePartsType,
  SheetRangePartsType,
  RangeIndicesType,
  RangeSpanType,
  ElementPositionType,
  CellsOptionsType,
  ColumnDimensionsOptionsType,
  RowDimensionsOptionsType
} from '~/types/grid'

const positionExp = /^[$]?([A-Za-z]{1,3})[$]?(\d+)$/
const sheetExp = /(?<sheet>([^'^!])*)?![$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/
const rangeExp = /[$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/

// Кеш преобразования 1 -> A
const __CACHE_COLUMN_PL: Record<number, string> = {}
// Кеш преобразования A -> 1
const __CACHE_COLUMN_LP: Record<string, number> = {}

/**
 * Преобразование числовой позиции в строковую
 * positionToLetter(1) -> 'A'
 * positionToLetter(26) -> 'Z'
 * positionToLetter(27) -> 'AA'
 * @param position числовая позиция
 */
const positionToLetter = (position: number): string => {
  if (position in __CACHE_COLUMN_PL) {
    return __CACHE_COLUMN_PL[position]
  }
  const base = 'Z'.charCodeAt(0) - 'A'.charCodeAt(0) + 1
  const letterCodes = []
  while (position > 0) {
    let remainder = position % base
    position = Math.floor(position / base)
    if (remainder === 0) {
      remainder = 26
      position -= 1
    }
    letterCodes.push(remainder + 'A'.charCodeAt(0) - 1)
  }
  const result = String.fromCharCode(...letterCodes.reverse())
  __CACHE_COLUMN_PL[position] = result
  return result
}

/**
 * Преобразование строковой позиции в числовую
 * letterToPosition('A') -> 1
 * letterToPosition('Z') -> 26
 * letterToPosition('AA') -> 27
 * @param letter строковая позиция
 */
const letterToPosition = (letter: string): number => {
  const l = letter.toUpperCase().replace(/[^A-Z]/gi, '')
  if (l in __CACHE_COLUMN_LP) {
    return __CACHE_COLUMN_LP[l]
  }
  const base = 'Z'.charCodeAt(0) - 'A'.charCodeAt(0) + 1
  const digits: number[] = l
    .split('')
    .map((e, i) => (e.charCodeAt(0) - 'A'.charCodeAt(0) + 1) * Math.pow(base, l.length - i - 1))
  const result = digits.reduce((a, c) => a + c, 0)
  __CACHE_COLUMN_LP[l] = result
  return result
}

/**
 * Разбор позиции на составляющие
 * parsePosition('A1') -> { column: 'A', row: 1 }
 * parsePosition('$A1') -> { column: 'A', row: 1 }
 * parsePosition('A$1') -> { column: 'A', row: 1 }
 * parsePosition('$A$1') -> { column: 'A', row: 1 }
 * @param position позиция
 */
const parsePosition = (position: string): PositionPartsType => {
  const match = position.match(positionExp)
  if (match === null) {
    throw new TypeError(`Неверный формат ячейки: ${position}`)
  }
  return { column: match[1], row: +match[2] }
}

/**
 * Разбор позиции с указанием sheet
 * parsePositionWithSheet('Лист!A1') -> { sheet: 'Лист', column: 'A', row: '1' }
 * @param position координата
 */
const parsePositionWithSheet = (position: string): SheetPositionPartsType => {
  const match = position.match(sheetExp)
  if (match === null) {
    throw new TypeError(`Неверный формат ячейки: ${position}`)
  }
  const { sheet, minColumn: column, minRow: row } = match.groups
  if (!(sheet && column && row)) {
    throw new TypeError(`Не удалось преобразовать координату: ${position}`)
  }
  return { sheet, column, row: parseInt(row) }
}

/**
 * Разбор диапазона
 * parseRange('A1:B2') -> { minColumn: 'A', minRow: 1, maxColumn: 'B', maxRow: 2 }
 * @param range диапазон
 */
const parseRange = (range: RangeType): RangePartsType => {
  const groups = range.match(rangeExp).groups
  const { minColumn, minRow, maxColumn, maxRow } = groups
  if (!(minColumn && minRow && maxColumn && maxRow)) {
    throw new TypeError(`Неверный формат диапазона: ${range}`)
  }
  // Проверить minColumn, minRow, maxColumn, maxRow на пустоту
  return { minColumn, minRow: parseInt(minRow), maxColumn, maxRow: parseInt(maxRow) }
}

/**
 * Разбор диапазона с указанием sheet
 * parseRangeWithSheet('Лист1!A1:B2') -> { sheet: 'Лист1', minColumn: 'A', minRow: '1', maxColumn: 'B', maxRow: '2' }
 * @param range диапазон
 */
const parseRangeWithSheet = (range: string): SheetRangePartsType => {
  const match = range.match(sheetExp)
  if (match === null) {
    throw new TypeError(`Неверный формат диапазона: ${range}`)
  }
  const { sheet, minColumn, minRow, maxColumn, maxRow } = match.groups
  if (!(sheet && minColumn && minRow && maxColumn && maxRow)) {
    throw new TypeError(`Не удалось преобразовать диапазон: ${range}`)
  }
  return { sheet, minColumn, minRow: parseInt(minRow), maxColumn, maxRow: parseInt(maxRow) }
}

/**
 * Преобразование набора позиций ячеек в числовое представление диапазона
 * positionsToRangeIndices(['A1', 'A2', 'B1', 'B2']) -> { minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }
 * positionsToRangeIndices(['A1', 'B2']) -> { minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }
 * positionsToRangeIndices(['A1']) -> { minColumn: 1, minRow: 1, maxColumn: 1, maxRow: 1 }
 * @param positions
 */
const positionsToRangeIndices = (positions: string[]): RangeIndicesType => {
  const rowsIndices: number[] = []
  const columnsIndices: number[] = []
  for (const position of positions) {
    const parsedPosition = parsePosition(position)
    rowsIndices.push(parsedPosition.row)
    columnsIndices.push(letterToPosition(parsedPosition.column))
  }
  return {
    minColumn: Math.min(...columnsIndices),
    minRow: Math.min(...rowsIndices),
    maxColumn: Math.max(...columnsIndices),
    maxRow: Math.max(...rowsIndices)
  }
}

/**
 * Преобразование диапазона в числовое представление
 * rangeToRangeIndices('A1:B2') -> { minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }
 * @param range диапазон
 */
const rangeToRangeIndices = (range: RangeType): RangeIndicesType => {
  const { minColumn, minRow, maxColumn, maxRow } = parseRange(range)
  const minColumnPosition = letterToPosition(minColumn)
  const maxColumnPosition = letterToPosition(maxColumn)
  return { minColumn: minColumnPosition, minRow, maxColumn: maxColumnPosition, maxRow }
}

/**
 * Преобразование числового представления диапазона в набор позиций ячеек
 * rangeIndicesToPositions({ minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }) -> ['A1', 'A2', 'B1', 'B2']
 * @param rangeIndices числовое представление диапазона
 */
const rangeIndicesToPositions = (rangeIndices: RangeIndicesType): string[] => {
  const cells: string[] = []
  for (let i = rangeIndices.minRow; i <= rangeIndices.maxRow; ++i) {
    for (let j = rangeIndices.minColumn; j <= rangeIndices.maxColumn; ++j) {
      cells.push(`${positionToLetter(j)}${i}`)
    }
  }
  return cells
}

/**
 * Преобразование диапазона в набор позиций входящих в него ячеек
 * rangeToCellPositions('A1:B2') -> ['A1', 'A2', 'B1', 'B2']
 * @param range диапазон
 */
const rangeToCellPositions = (range: RangeType): string[] => {
  return rangeIndicesToPositions(rangeToRangeIndices(range))
}

/**
 * Разбор диапазона на составляющие
 * rangeSpan('A1:B2') -> { target: 'A1', colspan: 2, rowSpan = 2, cells: ['A2', 'B1', 'B2'] }
 * @param range диапазон
 */
const rangeSpan = (range: RangeType): RangeSpanType => {
  const { minColumn, minRow, maxColumn, maxRow } = rangeToRangeIndices(range)
  const cells: string[] = rangeToCellPositions(range)
  const colspan: number = maxColumn - minColumn + 1
  const rowspan: number = maxRow - minRow + 1
  const target: string = cells.shift()
  return { target, colspan, rowspan, cells }
}

/**
 * Преобразование позиции элемента в стили
 * elementPositionToStyles({ left: 10, right: null, top: 10, bottom: null }) ->
 * { left: '10px', top: '10px' }
 * @param elementPosition
 */
const elementPositionToStyle = (elementPosition: ElementPositionType): Record<string, string> => {
  return Object.entries(elementPosition)
    .filter(([_, v]) => v !== null)
    .reduce((acc, [k, v]) => ({ ...acc, [k]: `${v}px` }), {})
}

/**
 * Фильтрация ячеек на листе
 * @param sheet
 * @param predicate
 */
const filterCells = (sheet: SheetType, predicate: (cell: CellType) => boolean): CellType[] => {
  const result: CellType[] = []
  for (const row of sheet.rows) {
    for (const cell of row.cells) {
      if (predicate(cell)) {
        result.push(cell)
      }
    }
  }
  return result
}

/**
 * Поиск ячейки на листе
 * @param sheet
 * @param predicate
 */
const findCell = (sheet: SheetType, predicate: (cell: CellType) => boolean): CellType | undefined => {
  for (const row of sheet.rows) {
    const cell = row.cells.find(predicate)
    if (cell) {
      return cell
    }
  }
  return undefined
}

/**
 * Получение связанных с объединением позиций в плоской структуре для массива ячеек
 * @param cells
 */
const getRelatedGlobalPositions = (cells: CellType[]): string[] => {
  return cells.reduce((a: string[], c: CellType) => {
    a.push(...c.relatedGlobalPositions)
    return a
  }, [])
}

/**
 * Объединение опций ячеек
 * @param options опции ячеек
 */
const uniteCellsOptions = <T>(options: T[]): T | null => {
  if (options.length === 0) {
    return null
  }
  const value = options[0]
  for (const val of options) {
    if (value !== val) {
      return null
    }
  }
  return value
}

/**
 * Получение опций ячеек
 * @param cells
 */
const getCellOptions = (cells: CellType[]): CellsOptionsType => {
  const possibleCellsOptions: (keyof CellsOptionsType)[] = [
    'strong', 'italic', 'strike',
    'underline', 'horizontalAlign', 'verticalAlign',
    'editable', 'size', 'kind',
    'numberFormat'
  ]
  const result: any = { cells }
  for (const option of possibleCellsOptions) {
    const options = []
    for (const cell of cells) {
      options.push(cell[option])
    }
    result[option] = uniteCellsOptions(options)
  }
  return result
}

/**
 * Получение опций колонок
 * @param columnDimensions
 * @param cells
 * @param rowsCount
 */
const getColumnDimensionsOptions = (
  columnDimensions: ColumnDimensionType[],
  cells: CellType[],
  rowsCount: number
): ColumnDimensionsOptionsType => {
  return {
    columnDimensions,
    fixed: columnDimensions.every((columnDimension: ColumnDimensionType) => columnDimension.fixed),
    rectangular: isColumnDimensionRectangular(columnDimensions, cells, rowsCount)
  }
}

/**
 * Является ли ячейки колонок прямоугольником
 * @param columnDimensions
 * @param cells
 * @param rowsCount
 */
const isColumnDimensionRectangular = (
  columnDimensions: ColumnDimensionType[],
  cells: CellType[],
  rowsCount: number
): boolean => {
  const relatedGlobalPositions = getRelatedGlobalPositions(cells)
  const rowsIndices = Array.from({ length: rowsCount }).map((_, i: number) => i + 1)
  for (const columnDimension of columnDimensions) {
    for (const rowIndex of rowsIndices) {
      const index = relatedGlobalPositions.indexOf(`${columnDimension.name}${rowIndex}`)
      if (index === -1) {
        return false
      }
      relatedGlobalPositions.splice(index, 1)
    }
  }
  return relatedGlobalPositions.length === 0
}

/**
 * Получение опций строк
 * @param rowDimensions
 * @param cells
 * @param columnsCount
 */
const getRowDimensionsOptions = (
  rowDimensions: RowDimensionType[],
  cells: CellType[],
  columnsCount: number
): RowDimensionsOptionsType => {
  return {
    rowDimensions,
    fixed: rowDimensions.every((rowDimension: RowDimensionType) => rowDimension.fixed),
    rectangular: isRowDimensionsRectangular(rowDimensions, cells, columnsCount)
  }
}

/**
 * Является ли ячейки строк прямоугольником
 * @param rowDimensions
 * @param cells
 * @param columnsCount
 */
const isRowDimensionsRectangular = (
  rowDimensions: RowDimensionType[],
  cells: CellType[],
  columnsCount: number
): boolean => {
  const relatedGlobalPositions = getRelatedGlobalPositions(cells)
  const columnsPositions = Array.from({ length: columnsCount })
    .map((_, i: number) => positionToLetter(i + 1))
  for (const rowDimension of rowDimensions) {
    for (const columnPosition of columnsPositions) {
      const index = relatedGlobalPositions.indexOf(`${columnPosition}${rowDimension.globalIndex}`)
      if (index === -1) {
        return false
      }
      relatedGlobalPositions.splice(index, 1)
    }
  }
  return relatedGlobalPositions.length === 0
}

/**
 * Получение стиля ширины ячейки
 * @param cell
 * @param getColumnWidth
 * @param activeSheet
 */
const getCellWidthStyle = (
  cell: CellType,
  getColumnWidth: (column: ColumnDimensionType) => number,
  activeSheet: SheetType
): Record<string, string> => {
  const { minColumn, maxColumn } = positionsToRangeIndices(cell.relatedGlobalPositions)
  let width = 0
  for (let i = minColumn - 1; i <= maxColumn - 1; i++) {
    width += getColumnWidth(activeSheet.columns[i])
  }
  return { width: `${width}px` }
}

/**
 * Получение стиля высоты ячейки
 * @param cell
 * @param getRowHeight
 * @param activeSheet
 */
const getCellHeightStyle = (
  cell: CellType,
  getRowHeight: (row: RowDimensionType) => number,
  activeSheet: SheetType
): Record<string, string> => {
  const { minRow, maxRow } = positionsToRangeIndices(cell.relatedGlobalPositions)
  let height = 0
  for (let i = minRow - 1; i <= maxRow - 1; i++) {
    height += getRowHeight(activeSheet.rows[i])
  }
  return { height: `${height}px` }
}

/**
 * Получение стилей для оформления текста ячейки
 * @param cell
 */
const getCellTextFormattingStyle = (cell: CellType): Record<string, string> => {
  const style: Record<string, string> = {}
  const textDecoration: string[] = []
  if (cell.strong) { style['font-weight'] = 'bold' }
  if (cell.italic) { style['font-style'] = 'italic' }
  if (cell.strike) { textDecoration.push('line-through') }
  if (cell.underline) { textDecoration.push('underline') }
  if (cell.size) { style['font-size'] = `${cell.size}pt` }
  if (textDecoration.length) {
    style['text-decoration'] = textDecoration.join(' ')
  }
  if (cell.error) {
    style.color = 'red'
  } else if (cell.color) {
    style.color = cell.color
  }
  return style
}

/**
 * Получение стилей для выравнивания текста ячейки
 * @param cell
 */
const getCellTextAlignmentStyle = (cell: CellType): Record<string, string> => {
  const style: Record<string, string> = {}
  if (cell.horizontalAlign) {
    style['text-align'] = cell.horizontalAlign
  }
  if (cell.verticalAlign) {
    style['vertical-align'] = cell.verticalAlign
  }
  return style
}

/**
 * Получение стилей для оформления границы ячейки
 * @param cell
 */
const getCellBorderStyle = (cell: CellType): Record<string, string> => {
  const style: Record<string, string> = {}
  const borderColor: Record<string, string | null> = JSON.parse(cell.borderColor)
  for (const position of ['top', 'right', 'bottom', 'left']) {
    if (borderColor[position]) {
      style[`border-${position}`] = `1px solid ${borderColor[position] || 'black'}`
    }
  }
  return style
}

/**
 * Получение стилей для оформления фона ячейки
 * @param cell
 * @param activeSheet
 */
const getCellBackgroundStyle = (cell: CellType, activeSheet: SheetType): Record<string, string> => {
  const style: Record<string, string> = {}
  const row = activeSheet.rows.find((row: RowDimensionType) => row.id === cell.rowId)
  if (cell.background && cell.background !== '#FFFFFF') {
    style.background = cell.background
  } else if (row.background) {
    style.background = row.background
  }
  return style
}

/**
 * Получение стилей ячейки, связанных с Excel
 * @param cell
 */
const getCellExcelStyle = (cell: CellType): Record<string, string> => {
  const style: Record<string, string> = {}
  if (cell.numberFormat) {
    style['mso-number-format'] = cell.numberFormat
  }
  return style
}

export {
  positionToLetter,
  letterToPosition,
  parsePosition,
  parsePositionWithSheet,
  parseRange,
  parseRangeWithSheet,
  positionsToRangeIndices,
  rangeToRangeIndices,
  rangeIndicesToPositions,
  rangeToCellPositions,
  rangeSpan,
  elementPositionToStyle,
  filterCells,
  findCell,
  getRelatedGlobalPositions,
  getCellOptions,
  getRowDimensionsOptions,
  getColumnDimensionsOptions,
  getCellWidthStyle,
  getCellHeightStyle,
  getCellTextFormattingStyle,
  getCellTextAlignmentStyle,
  getCellBorderStyle,
  getCellBackgroundStyle,
  getCellExcelStyle
}
