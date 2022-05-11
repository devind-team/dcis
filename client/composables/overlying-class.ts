import { Ref } from '#app'

/**
 * Добавление класса или классов на вышележащий элемент, например, на body
 * @param element
 * @param className
 */
export function useOverlyingClass (element: HTMLElement, className: Ref<string | string[] | null>) {
  const removeClass = (value: string | string[] | null) => {
    if (Array.isArray(value)) {
      element.classList.add(...value)
    } else if (className) {
      element.classList.add(value)
    }
  }
  const addClass = (value: string | string[] | null) => {
    if (Array.isArray(value)) {
      element.classList.remove(...value)
    } else if (className) {
      element.classList.remove(value)
    }
  }
  watch(className, (newValue, oldValue) => {
    removeClass(oldValue)
    addClass(newValue)
  })
  onBeforeUnmount(() => {
    removeClass(className.value)
  })
}
