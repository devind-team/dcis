import { CellType } from '~/types/graphql'
import { RangeIndicesType, RangePositionsType, RangeType } from '~/types/grid'

const rangeExp = /[$]?(?<minColumn>[A-Za-z]{1,3})?[$]?(?<minRow>\d+)?(:[$]?(?<maxColumn>[A-Za-z]{1,3})?[$]?(?<maxRow>\d+))?/

// Кеш преобразования 1 -> A
const __CACHE_COLUMN_PL: Record<number, string> = {}
// Кеш преобразования A -> 1
const __CACHE_COLUMN_LP: Record<string, number> = {}

/**
 * Преобразование числа в строку
 * positionToLetter(1) -> 'A'
 * positionToLetter(26) -> 'Z'
 * positionToLetter(27) -> 'AA'
 * @param position
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
 * Преобразование строки в число
 * letterToPosition('A') -> 1
 * letterToPosition('Z') -> 26
 * letterToPosition('AA') -> 27
 * @param letter
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
 * Нормализация диапазона
 * normalizationRange('A1:B2') -> 'A1:B2'
 * normalizationRange('B2:A1') -> 'A1:B2'
 * @param range
 */
const normalizeRange = (range: RangeType): RangeType => {
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
 * Парсинг диапазона
 * parseRange('A1:B2') -> { minColumn: 'A', minRow: 1, maxColumn: 'B', maxRow: 2 }
 * @param range
 */
const parseRange = (range: RangeType): RangePositionsType => {
  const groups = range.match(rangeExp).groups
  const { minColumn, minRow, maxColumn, maxRow } = groups
  if (!(minColumn && minRow && maxColumn && maxRow)) {
    throw new TypeError(`Неверный формат диапазона: ${range}`)
  }
  // Проверить minColumn, minRow, maxColumn, maxRow на пустоту
  return { minColumn, minRow: parseInt(minRow), maxColumn, maxRow: parseInt(maxRow) }
}

/**
 * Преобразование диапазона в числовое представление
 * rangeToPositions('A1:B2') -> { minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }
 * @param range
 */
const rangeToRangeIndices = (range: RangeType): RangeIndicesType => {
  const { minColumn, minRow, maxColumn, maxRow } = parseRange(range)
  const minColumnPosition = letterToPosition(minColumn)
  const maxColumnPosition = letterToPosition(maxColumn)
  return { minColumn: minColumnPosition, minRow, maxColumn: maxColumnPosition, maxRow }
}

/**
 * Преобразование числового представления диапазона в набор ячеек
 * rangeIndicesToCells({ minColumn: 1, minRow: 1, maxColumn: 2, maxRow: 2 }) -> ['A1', 'A2', 'B1', 'B2']
 * @param rangeIndices минимальная позиция строки
 */
const rangeIndicesToCells = (rangeIndices: RangeIndicesType): string[] => {
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
 * rangeLetterToCells('A1:B2') -> ['A1', 'A2', 'B1', 'B2']
 * @param range
 */
const rangeToCellPositions = (range: RangeType): string[] => {
  return rangeIndicesToCells(rangeToRangeIndices(normalizeRange(range)))
}

/**
 * Получение стилей ячейки
 * @param cell
 */
const getCellStyle = (cell: CellType): Record<string, string> => {
  const styles: Record<string, string> = {}
  if (cell.verticalAlign) { styles['vertical-align'] = cell.verticalAlign }
  if (cell.horizontalAlign) { styles['text-align'] = cell.horizontalAlign }
  if (cell.size) { styles['font-size'] = `${cell.size}px` }
  if (cell.strong) { styles['font-weight'] = 'bold' }
  if (cell.italic) { styles['font-style'] = 'italic' }
  if (cell.underline) { styles['text-decoration'] = 'underline' }
  if (cell.color) { styles['font-color'] = cell.color }
  if (cell.background) { styles['background-color'] = cell.background }
  const borderColor: Record<string, string | null> = JSON.parse(cell.borderColor)
  for (const position of ['top', 'right', 'bottom', 'left']) {
    if (borderColor[position]) {
      cell[`border-${position}`] = `1 px solid ${borderColor[position] || 'black'}`
    }
  }
  return styles
}

export {
  positionToLetter,
  letterToPosition,
  normalizeRange,
  parseRange,
  rangeToRangeIndices,
  rangeIndicesToCells,
  rangeToCellPositions,
  getCellStyle
}
