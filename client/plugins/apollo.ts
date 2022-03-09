import { InMemoryCache, IntrospectionFragmentMatcher } from 'apollo-cache-inmemory'
import { Plugin, Context } from '@nuxt/types'
import schema from '~/schema.json'

const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData: schema
})

export default <Plugin> function (context: Context): any {
  return {
    httpEndpoint: context.$config.API_URL,
    browserHttpEndpoint: context.$config.API_URL_BROWSER,
    wsEndpoint: context.$config.WS_URL,
    cache: new InMemoryCache({ fragmentMatcher }),
    httpLinkOptions: {
      headers: {
        'Accept-Language': 'ru' // Язык по умолчанию
      }
    }
  }
}
