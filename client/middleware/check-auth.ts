/**
 * Прослойка проверки авторзации
 * Если существует токен, сохраняем пользователя в кеш
 */

import { Context, Middleware } from '@nuxt/types'
import { useAuthStore } from '~/store/auth-store'
import { MeQuery, MeQueryVariables, UserType } from '~/types/graphql'
import meQuery from '~/gql/core/queries/me.graphql'

export default <Middleware> async function ({ app: { $apolloHelpers, apolloProvider }, store }: Context) {
  const hasToken = Boolean($apolloHelpers.getToken())
  const userStore = useAuthStore()
  if (hasToken && !userStore.loginIn) {
    const defaultClient = apolloProvider.defaultClient
    const user: UserType | null = await defaultClient.query<MeQuery, MeQueryVariables>({
      query: meQuery,
      fetchPolicy: 'network-only'
    }).then(({ data }) => data.me as UserType)
    if (user) {
      userStore.user = user as UserType
      await store.dispatch('auth/fetchExistUser', Object.assign({}, user)) // Убрать после удаления vuex
    } else {
      userStore.user = null
      await store.dispatch('auth/logout') // Убрать после удаления vuex
    }
  }
}
