/**
 * Прослойка проверки авторизации
 * Если существует токен, сохраняем пользователя в кеш
 */

import { Context, Middleware } from '@nuxt/types'
import { useAuthStore } from '~/stores'
import { MeQuery, MeQueryVariables, UserType } from '~/types/graphql'
import meQuery from '~/gql/core/queries/me.graphql'

export default <Middleware> async function ({ app: { $apolloHelpers, apolloProvider } }: Context) {
  const hasToken = Boolean($apolloHelpers.getToken())
  const authStore = useAuthStore()
  if (hasToken && !authStore.loginIn) {
    const defaultClient = apolloProvider.defaultClient
    const user: UserType | null = await defaultClient.query<MeQuery, MeQueryVariables>({
      query: meQuery,
      fetchPolicy: 'network-only'
    }).then(({ data }) => data.me as UserType)
    authStore.user = user ? user as UserType : null
  }
}
