/**
 * Прослойка переадресации на внешний ресурс
 * Переадресация на cbias.ru, в случае если пользователь не авторизован
 * и на главную страницу, если пользователь авторизован
 */
import { Middleware, Context } from '@nuxt/types'

export default <Middleware> function ({ redirect, app: { $apolloHelpers } }: Context) {
  const hasToken = Boolean($apolloHelpers.getToken())
  if (hasToken) {
    redirect('/')
  }
  redirect('https://cbias.ru')
}
