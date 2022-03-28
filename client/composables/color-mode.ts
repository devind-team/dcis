import { VueConstructor } from 'vue'
import { getCurrentInstance } from '#app'

export function useVuetify () {
  const instance = getCurrentInstance()
  const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>

  return {
    vuetify: vm.$vuetify,
    colorMode: vm.$colorMode,
    isDark: vm.$colorMode.value === 'dark'
  }
}
