import type { VueConstructor } from 'vue'
import type { WritableComputedRef } from '#app'
import { computed, getCurrentInstance } from '#app'

export function useVModel<T> (props, propName: string): WritableComputedRef<T> {
  const instance = getCurrentInstance()
  const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>

  return computed<T>({
    get: () => ((props[propName] as T)),
    set: (value: T) => (vm.$emit(`update:${propName}`, value))
  })
}
