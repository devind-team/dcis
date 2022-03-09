import ru from 'vuetify/es5/locale/ru'
import { Plugin, Context } from '@nuxt/types'

export default <Plugin> function ({ app: { vuetify } }: Context) {
  vuetify!.framework.lang.current = 'ru'
  vuetify!.framework.lang.locales = { ru }
  vuetify!.framework.theme.options = { ...vuetify!.framework.theme.options, customProperties: true }
}
