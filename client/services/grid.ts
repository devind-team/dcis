import { CellType } from '~/types/graphql'

// Кеш преобразования 1 -> A
const __CACHE_COLUMN_PL: Record<number, string> = {}
// Кеш преобразования A -> 1
const __CACHE_COLUMN_LP: Record<string, number> = {}

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
  getCellStyle
}
