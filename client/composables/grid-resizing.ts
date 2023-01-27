import { RemovableRef, useEventListener } from '@vueuse/core'
import { computed, ref, Ref, UnwrapRef } from '#app'
import { getDimensionSizeKey } from '~/composables/grid-local-mutations'
import {
  ElementPositionType,
  ElementResizingType,
  GridMode,
  MousePositionType,
  ResizingType,
  ScrollInfoType
} from '~/types/grid'
import { DocumentType } from '~/types/graphql'

export type DimensionType = {
  id: string,
  width?: number,
  height?: number,
  parent?: DimensionType | null
}

export function useGridResizing<T extends DimensionType> (
  scroll: Ref<ScrollInfoType>,
  defaultSize: number,
  direction: 'x' | 'y',
  changeSize: (dimension: T, size: number) => void | Promise<void>,
  dimensionSizeMap: RemovableRef<Record<string, number>>,
  mode: Ref<GridMode>,
  activeDocument: Ref<DocumentType>
) {
  const borderGag = 6

  const dimensionKey = direction === 'x' ? 'width' : 'height'
  const offsetSizeKey = direction === 'x' ? 'offsetWidth' : 'offsetHeight'
  const eventOffsetKey = direction === 'x' ? 'offsetX' : 'offsetY'

  const defaultElementSize = ref<number>(defaultSize)
  const resizing = ref<ResizingType<T> | null>(null)
  const elementPosition = ref<ElementPositionType>({ left: null, right: null, top: null, bottom: null })
  const elementResizing = computed<ElementResizingType>(() => ({
    visible: !!resizing.value && resizing.value.state === 'resizing',
    position: elementPosition.value,
    size: resizing.value ? resizing.value.size : 0
  }))

  const isRemoteSource = (dimension: T) => mode.value === GridMode.CHANGE || (
    direction === 'y' && mode.value !== GridMode.READ && dimension.parent !== null
  )

  const getSize = (dimension: T): number => {
    if (resizing.value && resizing.value.object.id === dimension.id) {
      return resizing.value.size
    }
    if (isRemoteSource(dimension)) {
      return dimension[dimensionKey] ?? defaultElementSize.value
    }
    const key = getDimensionSizeKey(activeDocument, dimension)
    return dimensionSizeMap.value[key] ?? dimension[dimensionKey] ?? defaultElementSize.value
  }

  const mousemove = (
    dimension: T,
    previousDimension: T | null,
    event: MouseEvent
  ) => {
    const mousePosition = { x: event.clientX, y: event.clientY }
    const cell = event.target as HTMLTableCellElement
    if (resizing.value && resizing.value.state === 'resizing') {
      resizing.value.size = Math.max(
        resizing.value.size + mousePosition[direction] - resizing.value.mousePosition[direction], 0
      )
      resizing.value.mousePosition = mousePosition
    } else if (cell[offsetSizeKey] - event[eventOffsetKey] < borderGag) {
      setResizingHover(dimension, mousePosition)
    } else if (
      cell[offsetSizeKey] - event[eventOffsetKey] > cell[offsetSizeKey] - borderGag &&
      previousDimension
    ) {
      setResizingHover(previousDimension, mousePosition)
    } else {
      resizing.value = null
    }
  }

  const mouseleave = () => {
    if (resizing.value && resizing.value.state === 'hover') {
      resizing.value = null
    }
  }

  const mousedown = (event: MouseEvent) => {
    if (resizing.value) {
      const target = event.target as HTMLDivElement | HTMLTableCellElement
      if (direction === 'x') {
        elementPosition.value = getElementPositionX(event, target)
      } else {
        elementPosition.value = getElementPositionY(event, target)
      }
      resizing.value.state = 'resizing'
    }
  }

  const mouseup = async () => {
    if (resizing.value) {
      resizing.value.state = 'hover'
      if (changeSize !== null) {
        await changeSize(resizing.value.object as T, resizing.value.size)
      }
    }
  }

  const getElementPositionX = (event: MouseEvent, target: HTMLDivElement | HTMLTableCellElement) => {
    const cell = target.closest('th')
    if (
      cell.offsetLeft - scroll.value.left +
      event.offsetX < document.body.offsetWidth - 150
    ) {
      return {
        left: cell.offsetLeft - scroll.value.left + event.offsetX,
        right: null,
        top: cell.offsetTop + event.offsetY - 25,
        bottom: null
      }
    } else {
      return {
        left: null,
        right: 25,
        top: cell.offsetTop + event.offsetY - 25,
        bottom: null
      }
    }
  }

  const getElementPositionY = (event: MouseEvent, target: HTMLDivElement | HTMLTableCellElement) => {
    const row = target.closest('tr')
    return {
      left: target.offsetLeft + event.offsetX,
      right: null,
      top: row.offsetTop - scroll.value.top + event.offsetY - 25,
      bottom: null
    }
  }

  const setResizingHover = (dimension: T, mousePosition: MousePositionType) => {
    const key = getDimensionSizeKey(activeDocument, dimension)
    let size = 0
    if (isRemoteSource(dimension)) {
      size = dimension[dimensionKey] ?? defaultElementSize.value
    } else {
      size = dimensionSizeMap.value[key] ?? dimension[dimensionKey] ?? defaultElementSize.value
    }
    resizing.value = {
      object: dimension as UnwrapRef<T>,
      size,
      mousePosition,
      state: 'hover'
    }
  }

  useEventListener('mouseup', async () => {
    if (resizing.value && resizing.value.state === 'resizing') {
      const res = resizing.value
      resizing.value = null
      if (changeSize !== null) {
        await changeSize(res.object as T, res.size)
      }
    }
  })

  useEventListener('mousemove', (event: MouseEvent) => {
    if (resizing.value && resizing.value.state === 'resizing') {
      const mousePosition = { x: event.clientX, y: event.clientY }
      resizing.value.size = Math.max(
        resizing.value.size + mousePosition[direction] - resizing.value.mousePosition[direction], 0
      )
      resizing.value.mousePosition = mousePosition
    }
  })

  return {
    resizing,
    elementResizing,
    getSize,
    mousemove,
    mouseleave,
    mousedown,
    mouseup
  }
}
