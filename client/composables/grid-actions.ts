import { computed, inject, Ref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  useAddRowDimensionMutation,
  useAddChildRowDimensionMutation,
  useDeleteRowDimensionMutation,
  useDeleteChildRowDimensionMutation,
  useChangeCellDefaultMutation,
  useChangeChildRowDimensionHeightMutation,
  useChangeColumnDimensionWidthMutation,
  useChangeFileValueMutation,
  useChangeRowDimensionHeightMutation,
  useChangeValueMutation,
  useUnloadFileValueArchiveMutation
} from '~/composables/grid-mutations'
import {
  GridModeInject,
  ActiveSheetInject,
  UpdateActiveSheetInject,
  ActiveDocumentInject,
  GridMode
} from '~/types/grid'
import {
  CellType,
  DocumentSheetQuery,
  PeriodSheetQuery,
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

export function useChangeColumnDimensionWidth () {
  const mode = inject(GridModeInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  if (mode.value === GridMode.CHANGE) {
    return useChangeColumnDimensionWidthMutation(updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>)
  }
  return null
}

export function useChangeRowDimensionHeight () {
  const mode = inject(GridModeInject)
  const updateActiveSheet = inject(UpdateActiveSheetInject)
  if (mode.value === GridMode.CHANGE) {
    return useChangeRowDimensionHeightMutation(updateActiveSheet as Ref<UpdateType<PeriodSheetQuery>>)
  }
  if (mode.value === GridMode.WRITE) {
    return useChangeChildRowDimensionHeightMutation(updateActiveSheet as Ref<UpdateType<DocumentSheetQuery>>)
  }
  return null
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
    return useChangeValueMutation(
      computed(() => activeDocument.value.id),
      computed(() => activeSheet.value.id)
    )
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