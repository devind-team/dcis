import { Ref } from '#app'
import { RemovableRef, useStorage } from '@vueuse/core'
import { DocumentType, ColumnDimensionType, RowDimensionType } from '~/types/graphql'

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

export function useChangeColumnDimensionWidthLocalMutation (
  columnDimensionWidthMap: RemovableRef<Record<string, number>>,
  activeDocument: Ref<DocumentType | null>
) {
  return function (columnDimension: ColumnDimensionType, width: number) {
    const key = activeDocument.value ? `${activeDocument.value.id}${columnDimension.id}` : columnDimension.id
    columnDimensionWidthMap.value = { ...columnDimensionWidthMap.value, [key]: width }
  }
}

export function useChangeRowDimensionHeightLocalMutation (
  rowDimensionHeightMap: RemovableRef<Record<string, number>>,
  activeDocument: Ref<DocumentType | null>
) {
  return function (rowDimension: RowDimensionType, height: number) {
    const key = activeDocument.value ? `${activeDocument.value.id}${rowDimension.id}` : rowDimension.id
    rowDimensionHeightMap.value = { ...rowDimensionHeightMap.value, [key]: height }
  }
}
