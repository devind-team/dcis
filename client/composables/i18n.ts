import { VueConstructor } from 'vue'
import { RawLocation } from 'vue-router'
import VueI18n from 'vue-i18n'
import type { WritableComputedRef } from '#app'
import { computed, getCurrentInstance, useNuxtApp } from '#app'

export interface Composer {
  locale: WritableComputedRef<string>,
  t: typeof VueI18n.prototype.t,
  tc: typeof VueI18n.prototype.tc,
  te: typeof VueI18n.prototype.te,
  d: typeof VueI18n.prototype.d,
  n: typeof VueI18n.prototype.n,
  localePath: (route: RawLocation, locale?: string) => string
}

export function useI18n (): Composer {
  const { $i18n } = useNuxtApp()
  const instance = getCurrentInstance()
  const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>
  const locale: WritableComputedRef<string> = computed({
    get () {
      return $i18n.locale
    },
    set (value: string) {
      $i18n.locale = value
    }
  })

  return {
    locale,
    t: vm.$t.bind(vm),
    tc: vm.$tc.bind(vm),
    te: vm.$te.bind(vm),
    d: vm.$d.bind(vm),
    n: vm.$n.bind(vm),
    localePath: vm.localePath.bind(vm)
  }
}
