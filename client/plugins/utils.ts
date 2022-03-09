import path from 'path'
import { ApolloClient } from 'apollo-client'
import accounting from 'accounting'
import { Context, Plugin } from '@nuxt/types'
import { Inject } from '@nuxt/types/app'
import type { Ref } from '#app'
import { isRef } from '#app'
import settingsQuery from '~/gql/core/queries/settings.graphql'
import { SettingType, UserType } from '~/types/graphql'
import { cursor, toGlobalId, fromGlobalId } from '~/services/graphql-relay'

export default <Plugin> async function ({ $config, app: { apolloProvider } }: Context, inject: Inject) {
  const apolloDefaultClient: ApolloClient<any> = apolloProvider?.defaultClient
  const { data: { settings } } = await apolloDefaultClient.query({ query: settingsQuery })
  inject('snakeToCamel', (str: string) => str.replace(
    /([-_][a-z])/g,
    (group: string) => group.toUpperCase()
      .replace('-', '')
      .replace('_', '')
  ))
  inject('getNowDate', () => {
    const nowDate = new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)
    return nowDate.toISOString().substr(0, 10)
  })
  inject('getUserName', (user: UserType | Ref<UserType>, showSirName: boolean = true) => {
    const u: UserType = isRef(user) ? user.value : user
    return `${u.lastName} ${u.firstName[0]}.${u.sirName && showSirName ? ' ' + u.sirName[0] + '.' : ''}`
  })
  inject('getUserFullName', (user: UserType | Ref<UserType>, showSirName: boolean = true) => {
    const u: UserType = isRef(user) ? user.value : user
    return `${u.lastName} ${u.firstName}${u.sirName && showSirName ? ' ' + u.sirName : ''}`
  })
  inject('filters', {
    money (str: string) {
      return accounting.formatNumber(str, 2, ' ', '.')
    },
    date (str: string) {
      if (str) {
        const time = str.split('T')
        return time[0].split('-').reverse().join('.')
      }
      return str
    },
    dateTimeHM (str: string) {
      const formatter = new Intl.DateTimeFormat('ru', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
      return formatter.format(new Date(str))
    },
    basename (str: string) {
      return path.basename(str)
    },
    textLength (str: string, length: number) {
      return str.slice(0, length) + (length < str.length ? '...' : '')
    },
    timeHM (str: string) {
      const formatter = new Intl.DateTimeFormat('ru', {
        hour: '2-digit',
        minute: '2-digit'
      })
      return formatter.format(new Date(str))
    }
  })
  inject('getSettingValue', (key: string) => {
    const s: SettingType | undefined = settings?.find((setting: SettingType) => setting.key === key)
    return s !== undefined ? s!.value : $config[key] || null
  })

  inject('fromGlobalId', fromGlobalId)
  inject('cursor', cursor)
  inject('toGlobalId', toGlobalId)
}
