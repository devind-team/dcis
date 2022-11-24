import { computed, inject, Ref } from '#app'
import { fromGlobalId } from '~/services/graphql-relay'
import { useAuthStore } from '~/stores'
import { GridModeInject, ActiveSheetInject, ActiveDocumentInject, GridMode } from '~/types/grid'
import { CellType, DivisionModelType, DocumentType, RowDimensionType } from '~/types/graphql'

export function useCanChangeRowHeight () {
  const userStore = useAuthStore()
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  return function (rowDimension: RowDimensionType) {
    if (mode.value === GridMode.CHANGE) {
      return true
    }
    if (mode.value === GridMode.READ) {
      return false
    }
    return rowDimension.parent !== null && (
      activeSheet.value.canChange ||
      activeSheet.value.canChangeChildRowDimensionHeight ||
      activeDocument.value.user?.id === userStore.user.id ||
      rowDimension.userId === String(fromGlobalId(userStore.user.id).id)
    )
  }
}

export function useCanChangeRowSettings () {
  const mode = inject(GridModeInject)
  return computed<boolean>(() => mode.value === GridMode.CHANGE)
}

export function useCanAddRowBeforeOrAfter () {
  const userStore = useAuthStore()
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  return function (rowDimension: RowDimensionType) {
    if (mode.value === GridMode.CHANGE) {
      return true
    }
    if (mode.value === GridMode.READ) {
      return false
    }
    if (rowDimension.parent) {
      const parent = activeSheet.value.rows.find((row: RowDimensionType) => rowDimension.parent.id === row.id)
      return parent.dynamic && (
        activeSheet.value.canChange ||
        activeSheet.value.canAddChildRowDimension ||
        activeDocument.value.user?.id === userStore.user.id ||
        canAddRowRegardingDivisions(userStore, activeDocument, rowDimension)
      )
    }
    return false
  }
}

export function useCanAddRowInside () {
  const userStore = useAuthStore()
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  return function (rowDimension: RowDimensionType) {
    if (mode.value === GridMode.READ || mode.value === GridMode.CHANGE) {
      return false
    }
    return rowDimension.dynamic && (
      activeSheet.value.canChange ||
      activeSheet.value.canAddChildRowDimension ||
      activeDocument.value.user?.id === userStore.user.id ||
      canAddRowRegardingDivisions(userStore, activeDocument, rowDimension)
    )
  }
}

export function useCanDeleteRow () {
  const userStore = useAuthStore()
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  const rootCount = computed<number>(() => activeSheet.value.rows
    .reduce((a: number, c: RowDimensionType) => c.parent ? a : a + 1, 0))
  return function (rowDimension: RowDimensionType) {
    if (mode.value === GridMode.CHANGE) {
      return rootCount.value !== 1 || Boolean(rowDimension.parent)
    }
    if (mode.value === GridMode.READ) {
      return false
    }
    return rowDimension.parent !== null && rowDimension.children.length === 0 && (
      activeSheet.value.canChange ||
      activeSheet.value.canDeleteChildRowDimension ||
      activeDocument.value.user?.id === userStore.user.id ||
      rowDimension.userId === String(fromGlobalId(userStore.user.id).id)
    )
  }
}

export function useCanChangeValue (cell: Ref<CellType>) {
  const userStore = useAuthStore()
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const activeDocument = inject(ActiveDocumentInject)
  return computed<boolean>(() => {
    if (mode.value === GridMode.CHANGE) {
      return true
    }
    if (mode.value === GridMode.READ || !cell.value.editable || cell.value.kind === 'f') {
      return false
    }
    if (
      activeSheet.value.canChange ||
      activeSheet.value.canChangeValue ||
      activeDocument.value.user?.id === userStore.user.id
    ) {
      return true
    }
    const userDivisionIds = userStore.user.divisions.map((division: DivisionModelType) => division.id)
    if (activeDocument.value.period.multiple) {
      return userDivisionIds.includes(activeDocument.value.objectId)
    }
    const row = activeSheet.value.rows.find((r: RowDimensionType) => r.id === cell.value.rowId)
    return userDivisionIds.includes(row.objectId)
  })
}

function canAddRowRegardingDivisions (
  userStore: ReturnType<typeof useAuthStore>,
  activeDocument: Ref<DocumentType | null>,
  rowDimension: RowDimensionType
) {
  const userDivisionIds = userStore.user.divisions.map((division: DivisionModelType) => division.id)
  if (activeDocument.value.period.multiple) {
    return userDivisionIds.includes(activeDocument.value.objectId)
  }
  return userDivisionIds.includes(rowDimension.objectId)
}
