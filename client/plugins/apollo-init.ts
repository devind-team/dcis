/**
 * Инициализация данных для apollo на стороне клиента
 * */
import { provideApolloClient } from '@vue/apollo-composable'
import { NuxtAppCompat } from '#app'

export default defineNuxtPlugin((nuxtApp: NuxtAppCompat) => {
  // @ts-ignore
  nuxtApp.hook('vue:setup', () => {
    // @ts-ignore
    const apolloClient = nuxtApp.nuxt2Context.app.apolloProvider.defaultClient
    provideApolloClient(apolloClient)
  })
})
