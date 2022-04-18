/**
 * Прослойка проверки авторизации
 * Если существует токен, сохраняем пользователя в кеш
 */

import { Context, Middleware } from '@nuxt/types'
import { useAuthStore } from '~/store/auth-store'
import { MeQuery, MeQueryVariables, UserType } from '~/types/graphql'
import meQuery from '~/gql/core/queries/me.graphql'

export default <Middleware> async function ({ app: { $apolloHelpers, apolloProvider }, store }: Context) {
  const hasToken = Boolean($apolloHelpers.getToken())
  const authStore = useAuthStore()
  if (hasToken && !authStore.loginIn) {
    const defaultClient = apolloProvider.defaultClient
    const user: UserType | null = await defaultClient.query<MeQuery, MeQueryVariables>({
      query: meQuery,
      fetchPolicy: 'network-only'
    }).then(({ data }) => data.me as UserType)
    if (user) {
      authStore.user = user as UserType
      await store.dispatch('auth/fetchExistUser', Object.assign({}, user)) // Убрать после удаления vuex
    } else {
      authStore.user = null
      await store.dispatch('auth/logout') // Убрать после удаления vuex
    }
  }
}
