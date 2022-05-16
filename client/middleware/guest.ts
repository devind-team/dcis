/**
 * Прослойка авторизации
 * Если пользователь не авторизован, пересылаем его на главную
 */

import { Middleware, Context } from '@nuxt/types'

export default <Middleware> function ({ redirect, app: { $apolloHelpers } }: Context) {
  const hasToken = Boolean($apolloHelpers.getToken())
  if (hasToken) {
    redirect('/')
  }
}
