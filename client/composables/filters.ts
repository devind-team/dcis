import path from 'path'
import accounting from 'accounting'
import { UserType } from '~/types/graphql'

export function useFilters () {
  const money = (s: string): string => accounting.formatNumber(s, 2, ' ', '.')

  const basename = (name: string): string => path.basename(name)

  const date = (rd: string): string => {
    if (rd) {
      const time = rd.split('T')
      return time[0].split('-').reverse().join('.')
    }
    return rd
  }

  const dateTimeHM = (rd: string): string => {
    const formatter = new Intl.DateTimeFormat('ru', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
    return formatter.format(new Date(rd))
  }

  const textLength = (text: string, length: number): string => text.slice(0, length) + (length < text.length ? '...' : '')

  const timeHM = (rd: string): string => {
    const formatter = new Intl.DateTimeFormat('ru', {
      hour: '2-digit',
      minute: '2-digit'
    })
    return formatter.format(new Date(rd))
  }

  const snakeToCamel = (value: string): string => value.replace(
    /([-_][a-z])/g,
    (group: string) => group.toUpperCase()
      .replace('-', '')
      .replace('_', '')
  )

  return { money, basename, date, dateTimeHM, timeHM, textLength, snakeToCamel }
}
