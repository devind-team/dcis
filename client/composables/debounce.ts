import defu from 'defu'
import { ref, unref, watch } from '#app'
import type { Ref } from '#app'
import { debouncedWatch } from '@vueuse/core'

export type DebounceCallbackFn = () => void | undefined
export type DebounceOptions = { debounce?: number, callback?: DebounceCallbackFn, defaultValue?: string }
export interface DebounceSearchInterface {
  search: Ref<string | null>
  debounceSearch: Ref<string | null>
}

export function useDebounceSearch (debounceOptions: DebounceOptions = {}): DebounceSearchInterface {
  const defaultOptions: DebounceOptions = {
    debounce: 700,
    callback: undefined,
    defaultValue: null
  }
  const { debounce, callback, defaultValue }: DebounceOptions = defu(debounceOptions, defaultOptions)

  const search: Ref<string | null> = ref<string | null>(unref(defaultValue))
  const debounceSearch: Ref<string | null> = ref<string | null>(unref(defaultValue))

  // Если у нас значение пустое, то устанавливаем сразу
  watch(search, () => {
    if (!search.value) {
      debounceSearch.value = search.value
    }
  })

  debouncedWatch(search, () => {
    if (callback) {
      callback()
    }
    debounceSearch.value = search.value
  }, { debounce })

  return { search, debounceSearch }
}
