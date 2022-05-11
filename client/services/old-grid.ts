import type { RangePositionsType, RangeSpanType, RangeType } from '~/types/grid-types'

const coordinateExp = /^[$]?([A-Za-z]{1,3})[$]?(\d+)$/
const sheetExp = /(?<sheet>([^'^!])*)?![$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/

/**
 * Разбираем координату на составляющие
 * parseCoordinate('A1') -> { column: 'A', row: 1 }
 * parseCoordinate('$A1') -> { column: 'A', row: 1 }
 * parseCoordinate('A$1') -> { column: 'A', row: 1 }
 * parseCoordinate('$A$1') -> { column: 'A', row: 1 }
 * @param coordinate
 */
const parseCoordinate = (coordinate: string): { column: string, row: number } => {
  const coordinateParse: object | null = coordinate.match(coordinateExp)
  if (coordinateParse === null) {
    throw new TypeError(`Неверный формат ячейки: ${coordinate}`)
  }
  const column: string = coordinateParse[1]
  const row: number = +coordinateParse[2]
  return { column, row }
}

/**
 * Преобразование диапазона в позицию
 * parseRangeToPosition('A1:B2') -> { minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }
 * @param range
 */
const parseRangeToPosition = (range: string): { minColumn: number, minRow: number, maxColumn: number, maxRow: number } => {
  const { minColumn, minRow, maxColumn, maxRow } = parseRange(range)
  return { minColumn: letterToPosition(minColumn), minRow, maxColumn: letterToPosition(maxColumn), maxRow }
}
/**
 * Парсинг координат с указанием sheet
 * parseCoordinateWithSheet('Лист!A1') -> { sheet: 'Лист', column: 'A', row: '1' }
 * @param coordinate Координата
 */
const parseCoordinateWithSheet = (coordinate: string): { sheet: string, column: string, row: number } => {
  const match = coordinate.match(sheetExp)
  if (match === null) {
    throw new TypeError(`Неверный формат ячейки: ${coordinate}`)
  }
  const { sheet, minColumn: column, minRow: row } = match.groups
  if (!(sheet && column && row)) {
    throw new TypeError(`Не удалось преобразовать координату: ${coordinate}`)
  }
  return { sheet, column, row: parseInt(row) }
}
/**
 * Парсим диапазон с указанием sheet
 * parseRangeWithSheet('Лист1!A1:B2') -> { sheet: 'Лист1', minColumn: 'A', minRow: '1', maxColumn: 'B', maxRow: '2' }
 * @param range диапазон
 */
const parseRangeWithSheet = (range: string): {
  sheet: string,
  minColumn: string,
  minRow: number,
  maxColumn: string,
  maxRow: number
} => {
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
 * Вспомогательная функция для применения действия к диапазону
 * @param rangePosition
 * @param callback
 */
const applyToRange = (rangePosition: RangePositionsType, callback: (column: number, row: number) => void) => {
  const { minColumn, minRow, maxColumn, maxRow } = rangePosition
  for (let i = minColumn; i <= maxColumn; ++i) {
    for (let j = minRow; j <= maxRow; ++j) {
      callback(i, j)
    }
  }
}

/**
 * Разбор диапазона на составляющие
 * rangeSpan('A1:B2') -> { target: 'A1', colspan: 2, rowSpan = 2, cells: ['A2', 'B1', 'B2'] }
 * @param range Нормализованный диапазон
 */
const rangeSpan = (range: RangeType): RangeSpanType => {
  const { minColumn, minRow, maxColumn, maxRow }: RangePositionsType = rangeToPositions(range)
  const cells: string[] = rangePositionToCells(minColumn, minRow, maxColumn, maxRow)
  const colspan: number = maxColumn - minColumn + 1
  const rowspan: number = maxRow - minRow + 1
  const target: string = cells.shift()
  return { target, colspan, rowspan, cells }
}

const unionValues = <T>(values: T[]): T | null => {
  if (values.length === 0) {
    return null
  }
  const value: T = values.shift()
  for (const val of values) {
    if (value !== val) {
      return null
    }
  }
  return value
}

export {
  parseCoordinate,
  parseRangeToPosition,
  parseCoordinateWithSheet,
  parseRangeWithSheet,
  rangeSpan,
  applyToRange,
  unionValues
}
