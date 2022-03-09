/**
 * Прослойка авторзации
 * Если пользователь не авторизован, пересылаем его на главную
 * Если у пользователя нет нужных разрешений, выбрасываем ошибку
 */

import Vue, { ComponentOptions } from 'vue'
import { Middleware, Context } from '@nuxt/types'
import { UserType } from '~/types/graphql'

export default <Middleware> function ({ redirect, app: { $apolloHelpers, localePath, i18n }, route, error, store }: Context) {
  const hasToken: boolean = Boolean($apolloHelpers.getToken())
  if (!hasToken) {
    redirect(localePath({ name: 'auth-login', query: { to: route.fullPath || undefined } }))
  }
  const permissions: string[] = ([] as (string | undefined)[]).concat(...route.matched.map((r: any) => {
    if (typeof r.components.default === 'function') {
      return (r.components.default as typeof Vue).options.permissions
    } else {
      return (r.components.default as ComponentOptions<Vue>).permissions
    }
  })).filter(p => p !== undefined) as string[]
  if (permissions.length !== 0 && !store.getters['auth/hasPerm'](permissions)) {
    return error({
      statusCode: 403,
      message: i18n.t('permissionDenied') as string
    })
  }
  if (store.getters['auth/loginIn'] && (store.getters['auth/user'] as UserType).agreement === null) {
    redirect(localePath({ name: 'auth-verification' }))
  }
}
