import { VueConstructor } from 'vue'
import { getCurrentInstance } from '#app'

export function useApolloHelpers () {
  const instance = getCurrentInstance()
  const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>

  return {
    getToken: vm.$apolloHelpers.getToken.bind(vm),
    onLogin: vm.$apolloHelpers.onLogin.bind(vm),
    onLogout: vm.$apolloHelpers.onLogout.bind(vm),
    defaultClient: vm.$apolloProvider.defaultClient
  }
}
