import { defineUserConfig } from '@vuepress/cli'
import { defaultTheme } from '@vuepress/theme-default'
import { registerComponentsPlugin } from '@vuepress/plugin-register-components'
import { path } from '@vuepress/utils'
import { navbarEn, navbarRu, sidebarEn, sidebarRu } from './configs'

export default defineUserConfig({
  base: '/dcis/',

  locales: {
    '/': {
      lang: 'ru-RU',
      title: 'Главная',
      description: 'Обычная документация',
    },
    '/en/': {
      lang: 'en-US',
      title: 'Home',
      description: 'Just playing around',
    },
  },

  theme: defaultTheme({
    repo: 'devind-team/dcis',
    docsDir: '/docs',

    locales: {
      '/': {
        navbar: navbarRu,
        selectLanguageName: 'Russian',
        selectLanguageText: 'Russian',
        selectLanguageAriaLabel: 'Russian',
        sidebar: sidebarRu
      },
      '/en/': {
        navbar: navbarEn,
        selectLanguageName: 'English',
        sidebar: sidebarEn
      }
    }

  }),

  plugins: [
    registerComponentsPlugin({
      componentsDir: path.resolve(__dirname, './components')
    })
  ]
})
