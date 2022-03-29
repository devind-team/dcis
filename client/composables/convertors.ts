import type { Ref } from '#app'
import { isRef } from '#app'
import { UserType } from '~/types/graphql'

export function useConvertors () {
  const snakeToCamel = (str: string) => str.replace(
    /([-_][a-z])/g,
    (group: string) => group.toUpperCase()
      .replace('-', '')
      .replace('_', '')
  )

  const getUserFullName = (user: UserType | Ref<UserType>, showSirName: boolean = true) => {
    const u: UserType = isRef(user) ? user.value : user
    return `${u.lastName} ${u.firstName}${u.sirName && showSirName ? ' ' + u.sirName : ''}`
  }

  const getUserName = (user: UserType | Ref<UserType>) => {
    const u: UserType = isRef(user) ? user.value : user
    return `${u.lastName} ${u.firstName[0]}.${u.sirName[0]}`
  }

  return { snakeToCamel, getUserFullName, getUserName }
}
