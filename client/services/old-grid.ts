import type { RangePositionsType, RangeSpanType, RangeType } from '~/types/grid-types'

const coordinateExp = /^[$]?([A-Za-z]{1,3})[$]?(\d+)$/
const rangeExp = /[$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/
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
 * Парсим диапазон
 * parseRange('A1:B2') -> { minColumn: 'A', minRow: 1, maxColumn: 'B', maxRow: 2 }
 * @param range
 */
const parseRange = (range: string): { minColumn: string, minRow: number, maxColumn: string, maxRow: number } => {
  const groups = range.match(rangeExp).groups
  const { minColumn, minRow, maxColumn, maxRow } = groups
  if (!(minColumn && minRow && maxColumn && maxRow)) {
    throw new TypeError(`Неверный формат диапазона: ${range}`)
  }
  // Проверить minColumn, minRow, maxColumn, maxRow на пустоту
  return { minColumn, minRow: parseInt(minRow), maxColumn, maxRow: parseInt(maxRow) }
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
 * Преобразования диапазона в числовое представление позиции
 * rangeToPositions('A1:B2') -> { minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }
 * @param range
 */
const rangeToPositions = (range: RangeType): RangePositionsType => {
  const { minColumn, minRow, maxColumn, maxRow } = parseRange(range)
  const minColumnPosition: number = letterToPosition(minColumn)
  const maxColumnPosition: number = letterToPosition(maxColumn)
  return { minColumn: minColumnPosition, minRow, maxColumn: maxColumnPosition, maxRow }
}
/**
 * Преобразование диапазона в набор ячеек
 * @param minColumn минимальная позиция строки
 * @param minRow минимальная позиция строки
 * @param maxColumn максимальная позиция колонки
 * @param maxRow максимальная позиция строки
 */
const rangePositionToCells = (
  minColumn: number,
  minRow: number,
  maxColumn: number,
  maxRow: number
): string[] => {
  const cells: string[] = []
  for (let i = minRow; i <= maxRow; ++i) {
    for (let j = minColumn; j <= maxColumn; ++j) {
      cells.push(`${positionToLetter(j)}${i}`)
    }
  }
  return cells
}
/**
 * Вспомогательная функция превращения диапазона в набор входящих в него ячеек
 * rangeLetterToCells('A1:B2') -> ['A1', 'A2', 'B1', 'B2']
 * @param range
 */
const rangeLetterToCells = (range: RangeType): string[] => {
  const { minColumn, minRow, maxColumn, maxRow }: RangePositionsType = rangeToPositions(normalizationRange(range))
  return rangePositionToCells(minColumn, minRow, maxColumn, maxRow)
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

/**
 * Нормализация диапазона
 * normalizationRange('A1:B2') -> 'A1:B2'
 * normalizationRange('B2:A1') -> 'A1:B2'
 * @param range Диапазон
 */
const normalizationRange = (range: RangeType): RangeType => {
  const { minColumn, minRow, maxColumn, maxRow } = parseRange(range)
  const minColumnPosition: number = letterToPosition(minColumn)
  const maxColumnPosition: number = letterToPosition(maxColumn)
  const minNormalizationColumn: string = positionToLetter(Math.min(minColumnPosition, maxColumnPosition))
  const maxNormalizationColumn: string = positionToLetter(Math.max(minColumnPosition, maxColumnPosition))
  const minNormalizationRow: number = Math.min(minRow, maxRow)
  const maxNormalizationRow: number = Math.max(minRow, maxRow)
  return `${minNormalizationColumn}${minNormalizationRow}:${maxNormalizationColumn}${maxNormalizationRow}`
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
  parseRange,
  parseRangeToPosition,
  parseCoordinateWithSheet,
  parseRangeWithSheet,
  rangePositionToCells,
  rangeSpan,
  rangeLetterToCells,
  applyToRange,
  normalizationRange,
  unionValues
}
