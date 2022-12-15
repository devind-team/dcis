import path from 'path'
import accounting from 'accounting'
import { Ref, unref } from '#app'
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
    return formatter.format(new Date(rd)).replace(',', '')
  }

  const textLength = (text: string, length: number): string => text.slice(0, length) + (length < text.length ? '...' : '')

  const timeHM = (rd: string): string => {
    const formatter = new Intl.DateTimeFormat('ru', {
      hour: '2-digit',
      minute: '2-digit'
    })
    return formatter.format(new Date(rd))
  }

  const getUserFullName = (user: UserType | Ref<UserType>, showSirName: boolean = true) => {
    const u = unref(user)
    return `${u.lastName} ${u.firstName}${u.sirName && showSirName ? ' ' + u.sirName : ''}`
  }

  const getUserName = (user: UserType | Ref<UserType>) => {
    const u = unref(user)
    return `${u.lastName} ${u.firstName[0]}.${u.sirName[0]}.`
  }

  return { money, basename, date, dateTimeHM, timeHM, textLength, getUserFullName, getUserName }
}
