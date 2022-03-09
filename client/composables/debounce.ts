import defu from 'defu'
import { useState, watch } from '#app'
import type { Ref } from '#app'
import { debouncedWatch } from '@vueuse/core'

export type DebounceCallbackFn = () => void | undefined
export type DebounceOptions = { debounce?: number, callback?: DebounceCallbackFn }
export interface DebounceSearchInterface {
  search: Ref<string | null>
  debounceSearch: Ref<string | null>
}

export function useDebounceSearch (debounceOptions: DebounceOptions = {}): DebounceSearchInterface {
  const defaultOptions: DebounceOptions = {
    debounce: 700,
    callback: undefined
  }
  const { debounce, callback }: DebounceOptions = defu(debounceOptions, defaultOptions)

  const search: Ref<string | null> = useState<string | null>('search', () => null)
  const debounceSearch: Ref<string | null> = useState<string | null>('debounceSearch', () => null)

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
