import Vue, { ComponentOptions } from 'vue'
import { SettingType, UserType } from '~/types/graphql'

declare module 'vue/types' {
  interface VueConstructor<V extends Vue = Vue> {
    options: ComponentOptions<V>
    permissions: string[]
  }
}

declare module 'vue/types/vue' {
  // this.$myInjectedFunction inside Vue components
  interface Vue {
    $getNowDate(): string
    $fromGlobalId(globalId: string): { type: string, id: string }
    $getSettingValue(key: string): string | null
    $getSettingValue(settings: SettingType[], key: string): string | null
    $cursor(n: number): string
    $toGlobalId(type: string, id: number): string
    $getUserName(user: UserType, showSirName?: boolean): string
    $getUserFullName(user: UserType, showSirName?: boolean): string
    $filters: {
      money(str: string): string,
      date(str: string): string,
      dateTimeHM(str: string): string,
      basename(str: string): string,
      textLength(str: string, length: number): string,
      timeHM(str: string): string
    }
  }
}

declare module 'vuex/types/index' {
  // this.$myInjectedFunction inside Vuex stores
  interface Store<S> {
    $getNowDate(): string
    $fromGlobalId(globalId: string): { type: string, id: string }
    $getSettingValue(key: string): string | null
    $cursor(n: number): string
    $toGlobalId(type: string, id: number): string
    $getUserName(user: UserType, showSirName?: boolean): string
    $getUserFullName(user: UserType, showSirName?: boolean): string
    $filters: {
      money(str: string): string,
      date(str: string): string,
      dateTimeHM(str: string): string,
      basename(str: string): string,
      textLength(str: string, length: number): string,
      timeHM(str: string): string
    }
  }
}

declare module 'vue/types/options' {
  // @ts-ignore
  interface ComponentOptions<V extends Vue> {
    permissions?: string | string[]
  }
}

declare module '@nuxt/types' {
  // nuxtContext.app.$myInjectedFunction inside asyncData, fetch, plugins, middleware, nuxtServerInit
  interface NuxtAppOptions {
    $getNowDate(): string
    $fromGlobalId(globalId: string): { type: string, id: string }
    $getSettingValue(key: string): string | null
    $cursor(n: number): string
    $toGlobalId(type: string, id: number): string
    $getUserName(user: UserType, showSirName?: boolean): string
    $getUserFullName(user: UserType, showSirName?: boolean): string
    $filters: {
      money(str: string): string,
      date(str: string): string,
      dateTimeHM(str: string): string,
      basename(str: string): string,
      textLength(str: string, length: number): string,
      timeHM(str: string): string
    }
  }
  // nuxtContext.$myInjectedFunction
  interface Context {
    $getNowDate(): string
    $getSettingValue(key: string): string | null
    $cursor(n: number): string
    $toGlobalId(type: string, id: number): string
    $fromGlobalId(globalId: string): { type: string, id: string }
    $getUserName(user: UserType, showSirName?: boolean): string
    $getUserFullName(user: UserType, showSirName?: boolean): string
    $filters: {
      money(str: string): string,
      date(str: string): string,
      dateTimeHM(str: string): string,
      basename(str: string): string,
      textLength(str: string, length: number): string,
      timeHM(str: string): string
    }
  }
}
