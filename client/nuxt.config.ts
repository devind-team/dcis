import { defineNuxtConfig } from '@nuxt/bridge'
import colors from 'vuetify/es5/util/colors'

export default defineNuxtConfig({
  app: {
    baseURL: '/'
  },
  bridge: {
    nitro: process.env.NODE_ENV === 'development'
  },
  alias: {
    tslib: 'tslib/tslib.es6.js'
  },
  /*
  ** Nuxt rendering mode
  ** See https://nuxtjs.org/api/configuration-mode
  */
  ssr: true,
  /*
  ** Nuxt target
  ** See https://nuxtjs.org/api/configuration-target
  */
  target: 'server',
  publicRuntimeConfig: {
    APP_NAME: process.env.APP_NAME,
    URL: process.env.URL,
    API_URL: process.env.API_URL,
    API_URL_BROWSER: process.env.API_URL_BROWSER,
    WS_URL: process.env.WS_URL,
    CLIENT_ID: process.env.CLIENT_ID,
    CLIENT_SECRET: process.env.CLIENT_SECRET,
    TINYMCE_API: process.env.TINYMCE_API,
    ASK: process.env.ASK
  },
  head: {
    title: 'Home page',
    titleTemplate: '%s - Информационная система сбора данных',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  loading: { color: '#413dff' },
  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '~/plugins/apollo-init',
    '~/plugins/utils',
    '~/plugins/vuetify',
    '~/plugins/vee-validate',
    '~/plugins/vue-i18n',
    { src: '~/plugins/rx', ssr: false },
    { src: '~/plugins/apex-chart', ssr: false }
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: false,

  buildModules: [
    '@nuxt/bridge',
    '@nuxtjs/vuetify',
    '@nuxtjs/i18n'
  ],
  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    ['@pinia/nuxt', { disableVuex: false }],
    '@nuxtjs/color-mode',
    '@nuxtjs/apollo',
    'cookie-universal-nuxt'
  ],
  apollo: {
    includeNodeModules: true,
    clientConfigs: {
      default: '~/plugins/apollo.ts'
    }
  },
  i18n: {
    lazy: true,
    langDir: 'lang/',
    defaultLocale: 'ru',
    detectBrowserLanguage: false,
    locales: [
      { code: 'ru', file: 'ru.ts' },
      { code: 'en', file: 'en.ts' }
    ]
  },
  typescript: {
    tsConfig: {
      compilerOptions: {
        experimentalDecorators: true,
        types: [
          '@types/node',
          '@nuxt/types',
          '@nuxtjs/color-mode',
          '@nuxtjs/i18n',
          'types',
          '@nuxt/content',
          '@nuxtjs/apollo/types',
          '@pinia/nuxt',
          'vuetify',
          'vue-apollo/types',
          'cookie-universal-nuxt',
          'vee-validate',
          '@nuxtjs/vuetify'
        ]
      }
    },
    // @ts-ignore
    typeCheck: {
      eslint: {
        files: './**/*.{ts,js,vue}'
      }
    }
  },
  router: {
    middleware: ['check-auth']
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    treeShake: true,
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },
  build: {
    parallel: true,
    transpile: [
      '@apollo/client',
      'graphql',
      'ts-invariant',
      'tslib',
      'vee-validate',
      'vee-validate/dist/rules',
      'subscriptions-transport-ws',
      'cross-fetch/polyfill',
      'cookie-universal-nuxt',
      'universal-cookie',
      'pinia'
    ]
  }
})
