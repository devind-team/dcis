import { Ref } from '#app'
import { RemovableRef, useStorage } from '@vueuse/core'
import { DocumentType, ColumnDimensionType, RowDimensionType } from '~/types/graphql'
import { DimensionType } from '~/composables/grid-resizing'

export function useColumnDimensionWidthMap () {
  return useStorage<Record<string, number>>(
    'column-dimension-width',
    {},
    localStorage,
    { listenToStorageChanges: true }
  )
}

export function useRowDimensionHeightMap () {
  return useStorage<Record<string, number>>(
    'row-dimension-height',
    {},
    localStorage,
    { listenToStorageChanges: true }
  )
}

export function getDimensionSizeKey<T extends DimensionType> (
  activeDocument: Ref<DocumentType | null>,
  dimension: T
) {
  return activeDocument.value ? `${activeDocument.value.id}${dimension.id}` : dimension.id
}

export function useChangeColumnDimensionWidthLocalMutation (
  columnDimensionWidthMap: RemovableRef<Record<string, number>>,
  activeDocument: Ref<DocumentType | null>
) {
  return function (columnDimension: ColumnDimensionType, width: number) {
    const key = getDimensionSizeKey(activeDocument, columnDimension)
    columnDimensionWidthMap.value = { ...columnDimensionWidthMap.value, [key]: width }
  }
}

export function useResetColumnDimensionWidthLocalMutation (
  columnDimensionWidthMap: RemovableRef<Record<string, number>>,
  activeDocument: Ref<DocumentType | null>
) {
  return function (columnDimension: ColumnDimensionType) {
    const key = getDimensionSizeKey(activeDocument, columnDimension)
    const { [key]: _, ...rest } = columnDimensionWidthMap.value
    columnDimensionWidthMap.value = rest
  }
}

export function useChangeRowDimensionHeightLocalMutation (
  rowDimensionHeightMap: RemovableRef<Record<string, number>>,
  activeDocument: Ref<DocumentType | null>
) {
  return function (rowDimension: RowDimensionType, height: number) {
    const key = getDimensionSizeKey(activeDocument, rowDimension)
    rowDimensionHeightMap.value = { ...rowDimensionHeightMap.value, [key]: height }
  }
}

export function useResetRowDimensionHeightLocalMutation (
  rowDimensionHeightMap: RemovableRef<Record<string, number>>,
  activeDocument: Ref<DocumentType | null>
) {
  return function (rowDimension: RowDimensionType) {
    const key = getDimensionSizeKey(activeDocument, rowDimension)
    const { [key]: _, ...rest } = rowDimensionHeightMap.value
    rowDimensionHeightMap.value = rest
  }
}
