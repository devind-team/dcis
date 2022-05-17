/**
 * Прослойка авторзации
 * Если пользователь не авторизован, пересылаем его на главную
 * Если у пользователя нет нужных разрешений, выбрасываем ошибку
 */

import Vue, { ComponentOptions } from 'vue'
import { Middleware, Context } from '@nuxt/types'
import { useAuthStore } from '~/stores'

export default <Middleware> function ({ redirect, app: { $apolloHelpers, localePath, i18n }, route, error }: Context) {
  const hasToken: boolean = Boolean($apolloHelpers.getToken())
  if (!hasToken) {
    redirect(localePath({ name: 'auth-login', query: { to: route.fullPath || undefined } }))
  }
  const permissions: string[] = ([] as (string | undefined)[]).concat(...route.matched.map((r: any) => {
    if (typeof r.components.default === 'function') {
      // @ts-ignore
      return (r.components.default as typeof Vue).options.permissions
    } else {
      // @ts-ignore
      return (r.components.default as ComponentOptions<Vue>).permissions
    }
  })).filter(p => p !== undefined) as string[]
  const authStore = useAuthStore()
  if (permissions.length !== 0 && !authStore.hasPerm(permissions)) {
    return error({
      statusCode: 403,
      message: i18n.t('permissionDenied') as string
    })
  }
  if (authStore.loginIn && authStore.user.agreement === null) {
    redirect(localePath({ name: 'auth-verification' }))
  }
}
