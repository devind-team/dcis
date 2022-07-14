import { InMemoryCache, IntrospectionFragmentMatcher } from 'apollo-cache-inmemory'
import { Plugin } from '@nuxt/types'
import { useRuntimeConfig } from '#app'
import schema from '~/schema.json'

const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData: schema
})

export default <Plugin> function (): any {
  const { API_URL, API_URL_BROWSER, WS_URL } = useRuntimeConfig()
  return {
    httpEndpoint: API_URL,
    browserHttpEndpoint: API_URL_BROWSER,
    wsEndpoint: WS_URL,
    cache: new InMemoryCache({ fragmentMatcher }),
    httpLinkOptions: {
      headers: {
        'Accept-Language': 'ru' // Язык по умолчанию
      }
    }
  }
}
