const __CACHE_COLUMN_PL: { [position: number]: string } = {} // Кеш преобразования 1 -> A
const __CACHE_COLUMN_LP: { [letter: string]: number } = {} // Кеш преобразования A -> 1

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

export {
  letterToPosition,
  positionToLetter
}
