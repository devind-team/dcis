import type { CellType, ValueType } from '~/types/graphql'
import type { RangePositionsType, RangeSpanType, RangeType } from '~/types/grid-types'

const coordinateExp = /^[$]?([A-Za-z]{1,3})[$]?(\d+)$/
const rangeExp = /[$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/
const sheetExp = /(?<sheet>([^'^!])*)?![$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/

// Кеш преобразования 1 -> A
const __CACHE_COLUMN_PL: { [position: number]: string } = {}
// Кеш преобразования A -> 1
const __CACHE_COLUMN_LP: { [letter: string]: number } = {}

/**
 * Разбираем координату на составляющие
 * parseCoordinate('A1') -> { column: 'A', row: '1' }
 * parseCoordinate('$A1') -> { column: 'A', row: '1' }
 * parseCoordinate('A$1') -> { column: 'A', row: '1' }
 * parseCoordinate('$A$1') -> { column: 'A', row: '1' }
 * @param coordinate
 */
const parseCoordinate = (coordinate: string): { column: string, row: number } => {
  const coordinateParse: object | null = coordinate.match(coordinateExp)
  if (coordinateParse === null) {
    throw new TypeError(`Неверный формат ячейки: ${coordinate}`)
  }
  const column: string = coordinateParse[1]
  const row: number = coordinateParse[2]
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

/**
 * Функция преобразования строки в число
 * letterToPosition('A') === 1
 * letterToPosition('Z') === 26
 * letterToPosition('AA') === 27
 * @param letters
 */
const letterToPosition = (letters: string): number => {
  const l: string = letters.toUpperCase().replace(/[^A-Z]/gi, '')
  if (l in __CACHE_COLUMN_LP) {
    return __CACHE_COLUMN_LP[l]
  }
  const base: number = 'Z'.charCodeAt(0) - 'A'.charCodeAt(0) + 1
  const digits: number[] = l
    .split('')
    .map((e, i) => (e.charCodeAt(0) - 'A'.charCodeAt(0) + 1) * Math.pow(base, l.length - i - 1))
  const result: number = digits.reduce((a, c) => a + c, 0)
  __CACHE_COLUMN_LP[l] = result
  return result
}

/**
 * Преобразование числа в строку
 * positionToLetter(1) === 'A'
 * positionToLetter(26) === 'Z'
 * positionToLetter(27) === 'AA'
 * @param position
 */
const positionToLetter = (position: number): string => {
  if (position in __CACHE_COLUMN_PL) {
    return __CACHE_COLUMN_PL[position]
  }
  const base: number = 'Z'.charCodeAt(0) - 'A'.charCodeAt(0) + 1
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
  const result: string = String.fromCharCode(...letterCodes.reverse())
  __CACHE_COLUMN_PL[position] = result
  return result
}

/**
 * Функция построения основных стилей
 * @param cell
 */
const getCellStyle = (cell: CellType): string => {
  const styles: string[] = []
  if (cell.verticalAlign) { styles.push(`text-align: ${cell.verticalAlign}`) }
  if (cell.horizontalAlign) { styles.push(`vertical-align: ${cell.verticalAlign}`) }
  if (cell.size) { styles.push(`font-size: ${cell.size}px`) }
  if (cell.strong) { styles.push('font-weight: bold') }
  if (cell.italic) { styles.push('font-style: italic') }
  if (cell.underline) { styles.push('text-decoration: underline') }
  return styles.join(';')
}

/**
 * Функция построения стилей для границ
 * @param cell
 */
const getCellBorder = (cell: CellType): string => {
  const borders: string[] = []
  try {
    const borderStyle: Record<string, string | null> = JSON.parse(cell.borderStyle)
    const borderColor: Record<string, string | null> = JSON.parse(cell.borderColor)
    for (const position of ['top', 'right', 'bottom', 'left']) {
      if (borderStyle[position] && ['thin', 'hair', 'medium'].includes(borderStyle[position])) {
        borders.push(`border-${position}: 1px solid ${borderColor[position] || ''}`.trimEnd())
      }
    }
  } catch { }
  return borders.join(';')
}

const getCellValue = (value: ValueType | undefined, cell: CellType): string => {
  return value ? value.value : cell.default
}

export {
  letterToPosition,
  positionToLetter,
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
  getCellStyle,
  getCellBorder,
  getCellValue
}
