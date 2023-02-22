import { computed, inject, Ref } from '#app'
import { RemovableRef } from '@vueuse/core'
import { UpdateType } from '~/composables/query-common'
import {
  useChangeColumnDimensionWidthLocalMutation,
  useChangeRowDimensionHeightLocalMutation,
  useResetColumnDimensionWidthLocalMutation,
  useResetRowDimensionHeightLocalMutation
} from '~/composables/grid-local-mutations'
import {
  useAddChildRowDimensionMutation,
  useAddRowDimensionMutation,
  useChangeCellDefaultMutation,
  useChangeChildRowDimensionHeightMutation,
  useChangeColumnDimensionWidthMutation,
  useChangeFileValueMutation,
  useChangeRowDimensionHeightMutation,
  useChangeValuesMutation,
  useDeleteChildRowDimensionMutation,
  useDeleteRowDimensionMutation,
  useUnloadFileValueArchiveMutation, ValueInputType, ValueStyleInputType
} from '~/composables/grid-mutations'
import { useCanChangeRowHeight } from '~/composables/grid-permissions'
import {
  ActiveDocumentInject,
  ActiveSheetInject,
  GridMode,
  GridModeInject,
  UpdateActiveSheetInject
} from '~/types/grid'
import {
  CellType,
  DocumentSheetQuery,
  PeriodSheetQuery,
  RowDimensionType,
  ValueFilesQuery
} from '~/types/graphql'

export function useAddRowDimension () {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  if (mode.value === GridMode.CHANGE) {
    return useAddRowDimensionMutation(
      activeSheet,
      updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>
    )
  }
  if (mode.value === GridMode.WRITE) {
    return useAddChildRowDimensionMutation(
      computed(() => activeDocument.value ? activeDocument.value.id : null),
      activeSheet,
      updateActiveSheet as Ref<UpdateType<DocumentSheetQuery>>
    )
  }
  return null
}

export function useDeleteRowDimension () {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  if (mode.value === GridMode.CHANGE) {
    return useDeleteRowDimensionMutation(activeSheet, updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>)
  }
  if (mode.value === GridMode.WRITE) {
    return useDeleteChildRowDimensionMutation(activeSheet, updateActiveSheet as Ref<UpdateType<DocumentSheetQuery>>)
  }
  return null
}

export function useChangeColumnDimensionWidth (columnDimensionWidthMap: RemovableRef<Record<string, number>>) {
  const mode = inject(GridModeInject)
  if (mode.value === GridMode.CHANGE) {
    const updateActiveSheet = inject(UpdateActiveSheetInject)
    return useChangeColumnDimensionWidthMutation(updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>)
  }
  const activeDocument = inject(ActiveDocumentInject)
  return useChangeColumnDimensionWidthLocalMutation(columnDimensionWidthMap, activeDocument)
}

export function useResetColumnDimensionWidth (columnDimensionWidthMap: RemovableRef<Record<string, number>>) {
  const activeDocument = inject(ActiveDocumentInject)
  return useResetColumnDimensionWidthLocalMutation(columnDimensionWidthMap, activeDocument)
}

export function useChangeRowDimensionHeight (rowDimensionHeightMap: RemovableRef<Record<string, number>>) {
  const mode = inject(GridModeInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  if (mode.value === GridMode.CHANGE) {
    return useChangeRowDimensionHeightMutation(updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>)
  }
  if (mode.value === GridMode.READ || mode.value === GridMode.WRITE) {
    const activeDocument = inject(ActiveDocumentInject)
    const canChangeRowHeight = useCanChangeRowHeight()
    const localMutation = useChangeRowDimensionHeightLocalMutation(rowDimensionHeightMap, activeDocument)
    const mutation = useChangeChildRowDimensionHeightMutation(updateActiveSheet as Ref<UpdateType<DocumentSheetQuery>>)
    return async function (rowDimension: RowDimensionType, height: number) {
      if (canChangeRowHeight(rowDimension)) {
        return await mutation(rowDimension, height)
      }
      return localMutation(rowDimension, height)
    }
  }
  return useChangeRowDimensionHeightLocalMutation(rowDimensionHeightMap, ref(null))
}

export function useResetRowDimensionHeight (rowDimensionHeightMap: RemovableRef<Record<string, number>>) {
  const activeDocument = inject(ActiveDocumentInject)
  return useResetRowDimensionHeightLocalMutation(rowDimensionHeightMap, activeDocument)
}

export function useChangeValue () {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  if (mode.value === GridMode.CHANGE) {
    return useChangeCellDefaultMutation(updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>)
  }
  if (mode.value === GridMode.WRITE) {
    const changeValues = useChangeValuesMutation(
      computed(() => activeDocument.value.id),
      computed(() => activeSheet.value.id)
    )
    return async function (cell: CellType, value: string) {
      await changeValues([{ cell, value }])
    }
  }
  return null
}

export function useChangeFileValue (cell: Ref<CellType>, updateFiles: UpdateType<ValueFilesQuery>) {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  if (mode.value === GridMode.WRITE) {
    return useChangeFileValueMutation(
      computed(() => activeDocument.value.id),
      computed(() => activeSheet.value.id),
      cell,
      updateActiveSheet as Ref<UpdateType<DocumentSheetQuery>>,
      updateFiles
    )
  }
  return null
}

export function useUnloadFileValueArchive (cell: Ref<CellType>) {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  if (mode.value === GridMode.WRITE) {
    return useUnloadFileValueArchiveMutation(
      computed(() => activeDocument.value ? activeDocument.value.id : ''),
      computed(() => activeSheet.value.id),
      cell
    )
  }
  return null
}

export function usePaste () {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  if (mode.value === GridMode.WRITE) {
    return {
      paste: useChangeValuesMutation(
        computed(() => activeDocument.value.id),
        computed(() => activeSheet.value.id)
      ),
      pasteWithStyles: null
    }
  }
  if (mode.value === GridMode.CHANGE) {
    return {
      paste: (values: ValueInputType[]) => {
        console.log(values)
      },
      pasteWithStyles: (values: ValueStyleInputType[]) => {
        console.log(values)
      }
    }
  }
  return null
}
