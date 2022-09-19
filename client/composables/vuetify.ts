import { VueConstructor } from 'vue'
import { computed, getCurrentInstance } from '#app'

export function useVuetify () {
  const instance = getCurrentInstance()
  const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>

  const isDark = computed<boolean>(() => (vm.$colorMode.value === 'dark'))
  return {
    vuetify: vm.$vuetify,
    colorMode: vm.$colorMode,
    isDark
  }
}
