import { useApolloClient, useMutation } from '@vue/apollo-composable'
import { ApolloClient, DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { Ref, unref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  AddChildRowDimensionMutation,
  AddChildRowDimensionMutationVariables,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  CellFieldsFragment,
  CellType,
  ChangeCellDefaultMutation,
  ChangeCellDefaultMutationVariables,
  ChangeCellsOptionMutation,
  ChangeCellsOptionMutationVariables,
  ChangeChildRowDimensionHeightMutation,
  ChangeChildRowDimensionHeightMutationVariables,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables,
  ChangeColumnDimensionsFixedMutation,
  ChangeColumnDimensionsFixedMutationVariables,
  ChangeFileValueMutation,
  ChangeFileValueMutationVariables,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables,
  ChangeRowDimensionsFixedMutation,
  ChangeRowDimensionsFixedMutationVariables,
  ChangeValueMutation,
  ChangeValueMutationVariables,
  ColumnDimensionFieldsFragment,
  ColumnDimensionType,
  DeleteChildRowDimensionMutation,
  DeleteChildRowDimensionMutationVariables,
  DeleteRowDimensionMutation,
  DeleteRowDimensionMutationVariables,
  DocumentSheetQuery,
  DocumentSheetQueryVariables,
  GlobalIndicesInputType,
  PeriodSheetQuery,
  RowDimensionFieldsFragment,
  RowDimensionType,
  SheetType,
  UnloadFileValueArchiveMutation,
  UnloadFileValueArchiveMutationVariables,
  ValueFilesQuery,
  ValueType
} from '~/types/graphql'
import { findCell, parsePosition } from '~/services/grid'
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import addChildRowDimensionMutation from '~/gql/dcis/mutations/document/add_child_row_dimension.graphql'
import deleteRowDimensionMutation from '~/gql/dcis/mutations/sheet/delete_row_dimension.graphql'
import deleteChildRowDimensionMutation from '~/gql/dcis/mutations/document/delete_child_row_dimension.graphql'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import changeColumnDimensionsFixedMutation from '~/gql/dcis/mutations/sheet/change_column_dimensions_fixed.graphql'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import changeRowDimensionsFixedMutation from '~/gql/dcis/mutations/sheet/change_row_dimensions_fixed.graphql'
import changeChildRowDimensionHeightMutation
  from '~/gql/dcis/mutations/document/change_child_row_dimension_height.graphql'
import changeCellDefaultMutation from '~/gql/dcis/mutations/cell/change_cell_default.graphql'
import changeCellsOptionMutation from '~/gql/dcis/mutations/cell/change_cells_option.graphql'
import changeValueMutation from '~/gql/dcis/mutations/values/change_value.graphql'
import changeFileValueMutation from '~/gql/dcis/mutations/values/change_file_value.graphql'
import unloadFileValueArchiveMutation from '~/gql/dcis/mutations/values/unload_file_value_archive.graphql'

export enum AddRowDimensionPosition {
  BEFORE,
  AFTER,
  INSIDE
}

export function useAddRowDimensionMutation (
  sheet: Ref<SheetType>,
  updateSheet: Ref<UpdateType<PeriodSheetQuery>>
) {
  const { mutate } = useMutation<
    AddRowDimensionMutation,
    AddRowDimensionMutationVariables
  >(addRowDimensionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) {
      if (result.data.addRowDimension.success) {
        updateSheet.value(
          dataProxy,
          result,
          (data: PeriodSheetQuery, {
            data: { addRowDimension: { rowDimension } }
          }: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) => {
            data.periodSheet.rows = addRow(sheet.value.columns, data.periodSheet.rows, rowDimension)
            return data
          })
      }
    }
  })
  return async function (rowDimension: RowDimensionType, position: AddRowDimensionPosition) {
    let variables: AddRowDimensionMutationVariables | Omit<
      AddRowDimensionMutationVariables, 'index' | 'globalIndex'
    > = {
      sheetId: sheet.value.id,
      globalIndices: collectGlobalIndices(sheet.value.rows, rowDimension)
    }
    if (position === AddRowDimensionPosition.BEFORE) {
      variables = { ...variables, index: rowDimension.index, globalIndex: rowDimension.globalIndex }
    } else if (position === AddRowDimensionPosition.AFTER) {
      const children = collectChildren(sheet.value.rows, [rowDimension.id])
        .sort((c1: RowDimensionType, c2: RowDimensionType) => c1.globalIndex - c2.globalIndex)
      variables = {
        ...variables,
        index: rowDimension.index + 1,
        globalIndex: children.at(-1).globalIndex + 1
      }
    }
    await mutate(variables as AddRowDimensionMutationVariables)
  }
}

export function useAddChildRowDimensionMutation (
  documentId: Ref<string>,
  sheet: Ref<SheetType>,
  updateSheet: Ref<UpdateType<DocumentSheetQuery>>
) {
  const { mutate } = useMutation<
    AddChildRowDimensionMutation,
    AddChildRowDimensionMutationVariables
  >(addChildRowDimensionMutation, {
    update (dateProxy: DataProxy, result: Omit<FetchResult<AddChildRowDimensionMutation>, 'context'>) {
      if (result.data.addChildRowDimension.success) {
        updateSheet.value(
          dateProxy,
          result,
          (data: DocumentSheetQuery, {
            data: { addChildRowDimension: { rowDimension } }
          }: Omit<FetchResult<AddChildRowDimensionMutation>, 'context'>) => {
            data.documentSheet.rows = addRow(sheet.value.columns, data.documentSheet.rows, rowDimension)
            return data
          }
        )
      }
    }
  })
  return async function (
    rowDimension: RowDimensionType,
    position: AddRowDimensionPosition
  ) {
    const parentRowDimension = rowDimension.parent
      ? sheet.value.rows.find((row: RowDimensionType) => rowDimension.parent.id === row.id)
      : null
    let variables: AddChildRowDimensionMutationVariables | Omit<
      AddChildRowDimensionMutationVariables, 'parentId' | 'index' | 'globalIndex'
    > = {
      documentId: documentId.value,
      sheetId: sheet.value.id,
      globalIndices: collectGlobalIndices(sheet.value.rows, rowDimension)
    }
    if (position === AddRowDimensionPosition.BEFORE) {
      variables = {
        ...variables,
        parentId: parentRowDimension.id,
        index: rowDimension.index,
        globalIndex: rowDimension.globalIndex
      }
    } else if (position === AddRowDimensionPosition.AFTER) {
      const children = collectChildren(sheet.value.rows, [rowDimension.id])
        .sort((c1: RowDimensionType, c2: RowDimensionType) => c1.globalIndex - c2.globalIndex)
      variables = {
        ...variables,
        parentId: parentRowDimension.id,
        index: rowDimension.index + 1,
        globalIndex: children.at(-1).globalIndex + 1
      }
    } else if (position === AddRowDimensionPosition.INSIDE) {
      const children = collectChildren(sheet.value.rows, [rowDimension.id])
        .sort((c1: RowDimensionType, c2: RowDimensionType) => c1.globalIndex - c2.globalIndex)
      variables = {
        ...variables,
        parentId: rowDimension.id,
        index: rowDimension.children.length ? rowDimension.children.at(-1).index + 1 : 1,
        globalIndex: children.at(-1).globalIndex + 1
      }
    }
    await mutate(variables as AddChildRowDimensionMutationVariables)
  }
}

export function useDeleteRowDimensionMutation (
  sheet: Ref<SheetType>,
  updateSheet: Ref<UpdateType<PeriodSheetQuery>>
) {
  const { mutate } = useMutation<
    DeleteRowDimensionMutation,
    DeleteRowDimensionMutationVariables
  >(deleteRowDimensionMutation)
  return async function (rowDimension: RowDimensionType) {
    await mutate({ rowDimensionId: rowDimension.id }, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<DeleteRowDimensionMutation>, 'context'>) {
        if (result.data.deleteRowDimension.success) {
          updateSheet.value(
            dataProxy,
            result,
            (
              data: PeriodSheetQuery, {
                data: { deleteRowDimension: { rowDimensionId } }
              }: Omit<FetchResult<DeleteRowDimensionMutation>, 'context'>
            ) => {
              data.periodSheet.rows = deleteRow(sheet.value.columns, data.periodSheet.rows, rowDimensionId)
              return data
            })
        }
      }
    })
  }
}

export function useDeleteChildRowDimensionMutation (
  sheet: Ref<SheetType>,
  updateSheet: Ref<UpdateType<DocumentSheetQuery>>
) {
  const { mutate } = useMutation<
    DeleteChildRowDimensionMutation,
    DeleteChildRowDimensionMutationVariables
  >(deleteChildRowDimensionMutation)
  return async function (rowDimension: RowDimensionType) {
    await mutate({ rowDimensionId: rowDimension.id }, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<DeleteChildRowDimensionMutation>, 'context'>) {
        if (result.data.deleteChildRowDimension.success) {
          updateSheet.value(
            dataProxy,
            result,
            (
              data: DocumentSheetQuery, {
                data: { deleteChildRowDimension: { rowDimensionId } }
              }: Omit<FetchResult<DeleteChildRowDimensionMutation>, 'context'>
            ) => {
              data.documentSheet.rows = deleteRow(sheet.value.columns, data.documentSheet.rows, rowDimensionId)
              return data
            }
          )
        }
      }
    })
  }
}

function addRow (
  columns: ColumnDimensionType[],
  rows: RowDimensionFieldsFragment[],
  newRow: RowDimensionFieldsFragment
): RowDimensionFieldsFragment[] {
  updateMergedCellsAdd(columns, rows, newRow)
  if (newRow.globalIndex === rows.at(-1).globalIndex + 1) {
    const newRows = [...rows, newRow]
    updateRelativeRows(newRows)
    return newRows
  }
  const newRows: RowDimensionFieldsFragment[] = []
  for (const row of rows) {
    if (row.globalIndex === newRow.globalIndex) {
      newRows.push(newRow)
    }
    if (row.globalIndex < newRow.globalIndex) {
      newRows.push(row)
    } else {
      row.globalIndex += 1
      if (row.index >= newRow.index && row.parent?.id === newRow.parent?.id) {
        row.index += 1
      }
      row.name = getRowName(rows, row)
      updateCellsPositions(row, (index: number) => index + 1)
      newRows.push(row)
    }
  }
  updateRelativeRows(newRows)
  return newRows
}

function deleteRow (
  columns: ColumnDimensionType[],
  rows: RowDimensionFieldsFragment[],
  deletedRowId: string
): RowDimensionFieldsFragment[] {
  const deletedRows = collectChildren(rows, [deletedRowId])
  updateMergedCellsDelete(columns, rows, deletedRows[0])
  const deletedGlobalIndices = deletedRows.map((r: RowDimensionFieldsFragment) => r.globalIndex)
  deletedGlobalIndices.sort((a: number, b: number) => a - b)
  const newRows: RowDimensionFieldsFragment[] = []
  for (const row of rows) {
    if (row.globalIndex < deletedGlobalIndices[0]) {
      newRows.push(row)
    } else if (row.globalIndex > deletedGlobalIndices.at(-1)) {
      row.globalIndex -= deletedGlobalIndices.length
      if (row.index >= deletedRows[0].index && row.parent?.id === deletedRows[0].parent?.id) {
        row.index -= 1
      }
      row.name = getRowName(rows, row)
      updateCellsPositions(row, (index: number) => index - deletedGlobalIndices.length)
      newRows.push(row)
    }
  }
  updateRelativeRows(newRows)
  return newRows
}

function updateMergedCellsAdd (
  columns: ColumnDimensionType[],
  rows: RowDimensionFieldsFragment[],
  newRow: RowDimensionFieldsFragment
): void {
  const missingPositions = getMissingPositions(columns, newRow)
  if (missingPositions.length) {
    updateMergedCells(
      rows,
      missingPositions,
      (cell: CellType) => { cell.rowspan += 1 },
      (cell: CellType, position: string) => { cell.relatedGlobalPositions.push(position) }
    )
  }
}

function updateMergedCellsDelete (
  columns: ColumnDimensionType[],
  rows: RowDimensionFieldsFragment[],
  deletedRow: RowDimensionFieldsFragment
): void {
  const missingPositions = getMissingPositions(columns, deletedRow)
  if (missingPositions.length) {
    updateMergedCells(
      rows,
      missingPositions,
      (cell: CellType) => { cell.rowspan -= 1 },
      (cell: CellType, position: string) => {
        cell.relatedGlobalPositions.splice(cell.relatedGlobalPositions.indexOf(position))
      }
    )
  }
}

function getMissingPositions (columns: ColumnDimensionType[], row: RowDimensionFieldsFragment): string[] {
  const cellsColumns = row.cells.map((cell: CellType) => parsePosition(cell.globalPosition).column)
  return columns
    .filter((column: ColumnDimensionType) => !cellsColumns.includes(column.name))
    .map((column: ColumnDimensionType) => `${column.name}${row.name}`)
}

function updateMergedCells (
  rows: RowDimensionFieldsFragment[],
  missingPositions: string[],
  updateCell: (cell: CellType) => void,
  updateCellRelatedGlobalPositions: (cell: CellType, position: string) => void
) {
  for (const row of rows) {
    for (const cell of row.cells) {
      const cellPositions = missingPositions.filter((p: string) => cell.relatedGlobalPositions.includes(p))
      if (cellPositions.length) {
        updateCell(cell)
        const { row: lastRow } = parsePosition(cell.relatedGlobalPositions.at(-1))
        for (const position of cellPositions) {
          const { column } = parsePosition(position)
          updateCellRelatedGlobalPositions(cell, `${column}${lastRow}`)
        }
      }
    }
  }
}

function collectGlobalIndices (
  rows: RowDimensionType[],
  row: RowDimensionType | null | undefined,
  globalIndices: GlobalIndicesInputType[] | null = null
): GlobalIndicesInputType[] {
  globalIndices = globalIndices || []
  if (!row) {
    return globalIndices
  }
  return collectGlobalIndices(
    rows,
    rows.find((r: RowDimensionType) => r.id === row.parent?.id),
    [...globalIndices, { rowId: row.id, globalIndex: row.globalIndex }]
  )
}

function collectChildren<T extends { id: string, children: { id: string }[]}> (
  rows: T[],
  rowsIds: string[]
): T[] {
  const rootRows: T[] = []
  for (const id of rowsIds) {
    rootRows.push(rows.find((r: T) => r.id === id))
  }
  const result = [...rootRows]
  for (const deletedRow of rootRows) {
    result.push(...collectChildren(rows, deletedRow.children.map(r => r.id)))
  }
  return result
}

function getRowName (
  rows: RowDimensionFieldsFragment[],
  row: RowDimensionFieldsFragment,
  indices: string[] | null = null
): string {
  indices = indices || []
  if (row.parent) {
    return getRowName(
      rows,
      rows.find((r: RowDimensionFieldsFragment) => r.id === row.parent.id),
      [String(row.index), ...indices]
    )
  }
  return [String(row.index), ...indices].join('.')
}

function updateCellsPositions (
  row: RowDimensionFieldsFragment,
  updateRelatedRowIndex: (index: number) => number
): void {
  for (const cell of row.cells) {
    const { column } = parsePosition(cell.globalPosition)
    cell.position = `${column}${row.name}`
    cell.globalPosition = `${column}${row.globalIndex}`
    cell.relatedGlobalPositions = cell.relatedGlobalPositions.map((position: string) => {
      const parsedPosition = parsePosition(position)
      return `${parsedPosition.column}${updateRelatedRowIndex(parsedPosition.row)}`
    })
  }
}

function updateRelativeRows (rows: RowDimensionFieldsFragment[]): void {
  for (const row of rows) {
    const newChildren: RowDimensionFieldsFragment['children'] = []
    for (const child of row.children) {
      const sourceChild = rows.find((r: RowDimensionFieldsFragment) => r.id === child.id)
      if (sourceChild) {
        child.index = sourceChild.index
        child.globalIndex = sourceChild.globalIndex
        newChildren.push(child)
      }
    }
    row.children = newChildren
    if (row.parent) {
      const sourceParent = rows.find((r: RowDimensionFieldsFragment) => r.id === row.parent.id)
      row.parent.index = sourceParent.index
      row.parent.globalIndex = sourceParent.globalIndex
      if (!sourceParent.children.find((r: RowDimensionFieldsFragment) => r.id === row.id)) {
        sourceParent.children.splice(row.index - 1, 0, {
          __typename: 'RowDimensionType',
          id: row.id,
          index: row.index,
          globalIndex: row.globalIndex
        })
      }
    }
  }
}

export function useChangeColumnDimensionWidthMutation (updateSheet: Ref<UpdateType<PeriodSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeColumnDimensionMutation,
    ChangeColumnDimensionMutationVariables
  >(changeColumnDimensionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>) {
      updateColumnDimension(updateSheet.value, dataProxy, result)
    }
  })
  return async function (columnDimension: ColumnDimensionType, width: number) {
    const variables: ChangeColumnDimensionMutationVariables = {
      columnDimensionId: columnDimension.id,
      width,
      hidden: columnDimension.hidden,
      kind: columnDimension.kind
    }
    await mutate(variables, {
      optimisticResponse: {
        __typename: 'Mutation',
        changeColumnDimension: {
          __typename: 'ChangeColumnDimensionMutationPayload',
          success: true,
          errors: [],
          columnDimension: {
            ...variables,
            id: columnDimension.id,
            updatedAt: new Date().toISOString(),
            __typename: 'ChangeColumnDimensionType'
          }
        }
      }
    })
  }
}

export function useChangeColumnDimensionsFixedMutation (updateSheet: Ref<UpdateType<PeriodSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeColumnDimensionsFixedMutation,
    ChangeColumnDimensionsFixedMutationVariables
  >(changeColumnDimensionsFixedMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeColumnDimensionsFixedMutation>, 'context'>) {
      if (result.data.changeColumnDimensionsFixed.success) {
        updateSheet.value(
          dataProxy,
          result, (
            data: PeriodSheetQuery,
            { data: { changeColumnDimensionsFixed } }: Omit<FetchResult<ChangeColumnDimensionsFixedMutation>, 'context'>
          ) => {
            for (const column of changeColumnDimensionsFixed.columnDimensions) {
              const columnDimension = data.periodSheet.columns.find(
                (columnDimension: ColumnDimensionFieldsFragment) => columnDimension.id === column.id
              )
              columnDimension.fixed = column.fixed
              columnDimension.updatedAt = column.updatedAt
            }
            return data
          }
        )
      }
    }
  })
  return async function (columnDimensions: ColumnDimensionType[], fixed: boolean) {
    await mutate({
      columnDimensionIds: columnDimensions.map((columnDimension: ColumnDimensionType) => columnDimension.id),
      fixed
    }, {
      optimisticResponse: {
        __typename: 'Mutation',
        changeColumnDimensionsFixed: {
          __typename: 'ChangeColumnDimensionsFixedPayload',
          success: true,
          errors: [],
          columnDimensions: columnDimensions.map((columnDimension: ColumnDimensionType) => ({
            id: columnDimension.id,
            fixed,
            updatedAt: new Date().toISOString(),
            __typename: 'ChangeColumnDimensionType'
          }))
        }
      }
    })
  }
}

export function updateColumnDimension (
  updateSheet: UpdateType<PeriodSheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>
) {
  if (result.data.changeColumnDimension.success) {
    updateSheet(
      dataProxy,
      result,
      (
        data: PeriodSheetQuery,
        { data: { changeColumnDimension } }: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>
      ) => {
        const columnDimension = data.periodSheet.columns.find((columnDimension: ColumnDimensionFieldsFragment) =>
          columnDimension.id === changeColumnDimension.columnDimension.id)!
        columnDimension.width = changeColumnDimension.columnDimension.width
        columnDimension.hidden = changeColumnDimension.columnDimension.hidden
        columnDimension.kind = changeColumnDimension.columnDimension.kind
        columnDimension.updatedAt = changeColumnDimension.columnDimension.updatedAt
        return data
      }
    )
  }
}

export function useChangeRowDimensionHeightMutation (updateSheet: Ref<UpdateType<PeriodSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeRowDimensionMutation,
    ChangeRowDimensionMutationVariables
  >(changeRowDimensionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>) {
      updateRowDimension(updateSheet.value, dataProxy, result)
    }
  })
  return async function (rowDimension: RowDimensionType, height: number) {
    const variables: ChangeRowDimensionMutationVariables = {
      rowDimensionId: rowDimension.id,
      height,
      hidden: rowDimension.hidden,
      dynamic: rowDimension.dynamic
    }
    await mutate(variables, {
      optimisticResponse: {
        __typename: 'Mutation',
        changeRowDimension: {
          __typename: 'ChangeRowDimensionMutationPayload',
          success: true,
          errors: [],
          rowDimension: {
            ...variables,
            id: rowDimension.id,
            updatedAt: new Date().toISOString(),
            __typename: 'ChangeRowDimensionType'
          }
        }
      }
    })
  }
}

export function useChangeChildRowDimensionHeightMutation (updateSheet: Ref<UpdateType<DocumentSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeChildRowDimensionHeightMutation,
    ChangeChildRowDimensionHeightMutationVariables
  >(changeChildRowDimensionHeightMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeChildRowDimensionHeightMutation>, 'context'>) {
      if (result.data.changeChildRowDimensionHeight.success) {
        updateSheet.value(
          dataProxy,
          result, (
            data: DocumentSheetQuery,
            { data: { changeChildRowDimensionHeight } }: Omit<FetchResult<ChangeChildRowDimensionHeightMutation>, 'context'>
          ) => {
            const rowDimension = data.documentSheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
              rowDimension.id === changeChildRowDimensionHeight.rowDimensionId)!
            rowDimension.height = changeChildRowDimensionHeight.height
            rowDimension.updatedAt = changeChildRowDimensionHeight.updatedAt
            return data
          }
        )
      }
    }
  })
  return async function (rowDimension: RowDimensionType, height: number) {
    const variables: ChangeChildRowDimensionHeightMutationVariables = {
      rowDimensionId: rowDimension.id,
      height
    }
    await mutate(variables, {
      optimisticResponse: {
        __typename: 'Mutation',
        changeChildRowDimensionHeight: {
          __typename: 'ChangeChildRowDimensionHeightMutationPayload',
          success: true,
          errors: [],
          ...variables,
          updatedAt: new Date().toISOString()
        }
      }
    })
  }
}

export function useChangeRowDimensionsFixedMutation (updateSheet: Ref<UpdateType<PeriodSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeRowDimensionsFixedMutation,
    ChangeRowDimensionsFixedMutationVariables
  >(changeRowDimensionsFixedMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeRowDimensionsFixedMutation>, 'context'>) {
      if (result.data.changeRowDimensionsFixed.success) {
        updateSheet.value(
          dataProxy,
          result, (
            data: PeriodSheetQuery,
            { data: { changeRowDimensionsFixed } }: Omit<FetchResult<ChangeRowDimensionsFixedMutation>, 'context'>
          ) => {
            for (const row of changeRowDimensionsFixed.rowDimensions) {
              const rowDimension = data.periodSheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
                rowDimension.id === row.id)!
              rowDimension.fixed = row.fixed
              rowDimension.updatedAt = row.updatedAt
            }
            return data
          }
        )
      }
    }
  })
  return async function (rowDimensions: RowDimensionType[], fixed: boolean) {
    await mutate({
      rowDimensionIds: rowDimensions.map((rowDimension: RowDimensionType) => rowDimension.id),
      fixed
    }, {
      optimisticResponse: {
        __typename: 'Mutation',
        changeRowDimensionsFixed: {
          __typename: 'ChangeRowDimensionsFixedPayload',
          success: true,
          errors: [],
          rowDimensions: rowDimensions.map((rowDimension: RowDimensionType) => ({
            id: rowDimension.id,
            fixed,
            updatedAt: new Date().toISOString(),
            __typename: 'ChangeRowDimensionType'
          }))
        }
      }
    })
  }
}

export function updateRowDimension (
  updateSheet: UpdateType<PeriodSheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
) {
  if (result.data.changeRowDimension.success) {
    updateSheet(
      dataProxy,
      result,
      (
        data: PeriodSheetQuery,
        { data: { changeRowDimension } }: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
      ) => {
        const rowDimension = data.periodSheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
          rowDimension.id === changeRowDimension.rowDimension.id)!
        rowDimension.height = changeRowDimension.rowDimension.height
        rowDimension.hidden = changeRowDimension.rowDimension.hidden
        rowDimension.dynamic = changeRowDimension.rowDimension.dynamic
        rowDimension.updatedAt = changeRowDimension.rowDimension.updatedAt
        return data
      }
    )
  }
}

export function useChangeCellDefaultMutation (updateSheet: Ref<UpdateType<PeriodSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeCellDefaultMutation,
    ChangeCellDefaultMutationVariables
  >(changeCellDefaultMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeCellDefaultMutation>, 'context'>) {
      if (result.data.changeCellDefault.success) {
        updateSheet.value(dataProxy, result, (
          data: PeriodSheetQuery, {
            data: { changeCellDefault }
          }: Omit<FetchResult<ChangeCellDefaultMutation>, 'context'>
        ) => {
          const cell = findCell(
            data.periodSheet as SheetType,
            (c: CellType) => c.id === changeCellDefault.cellId
          )
          cell.value = changeCellDefault.default
          return data
        })
      }
    }
  })
  return async function (cell: CellType, defaultValue: string) {
    await mutate({
      cellId: cell.id,
      default: defaultValue
    }, {
      optimisticResponse: {
        __typename: 'Mutation',
        changeCellDefault: {
          __typename: 'ChangeCellDefaultPayload',
          success: true,
          errors: [],
          cellId: cell.id,
          default: defaultValue
        }
      }
    })
  }
}

export function useChangeCellsOptionMutation (updateSheet: Ref<UpdateType<PeriodSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeCellsOptionMutation,
    ChangeCellsOptionMutationVariables
  >(changeCellsOptionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeCellsOptionMutation>, 'context'>) {
      if (result.data.changeCellsOption.success) {
        updateSheet.value(dataProxy, result, (
          data: PeriodSheetQuery, {
            data: { changeCellsOption: { changedOptions } }
          }: Omit<FetchResult<ChangeCellsOptionMutation>, 'context'>
        ) => {
          for (const option of changedOptions) {
            const cell = findCell(
              data.periodSheet as SheetType,
              (c: CellType) => c.id === option.cellId
            )
            if (option.field === 'size') {
              cell[option.field] = Number(option.value)
            } else if (['strong', 'italic', 'strike', 'editable'].includes(option.field)) {
              cell[option.field] = option.value === 'true'
            } else {
              cell[option.field] = option.value
            }
          }
          return data
        })
      }
    }
  })
  return async function (cells: CellType[], field: string, value: string) {
    await mutate({
      cellIds: cells.map((cell: CellType) => cell.id.toString()),
      field,
      value
    })
  }
}

export const changeSheetValues = (
  values: ValueType[],
  client: ApolloClient<DocumentSheetQuery>,
  documentId: Ref<string | null> | string, updatedAt: string | null = null
) => {
  const sheetValue = values.reduce<Record<number, ValueType[]>>((a, v) => {
    if (!(v.sheetId in a)) { a[v.sheetId] = [] }
    a[v.sheetId].push(v)
    return a
  }, {})
  for (const [sid, vs] of Object.entries(sheetValue)) {
    try {
      const data = client.readQuery<DocumentSheetQuery, DocumentSheetQueryVariables>({
        query: documentSheetQuery,
        variables: {
          documentId: unref(documentId),
          sheetId: sid
        }
      })
      updateValues(data, vs, updatedAt)
      client.writeQuery<DocumentSheetQuery, DocumentSheetQueryVariables>({
        query: documentSheetQuery,
        variables: {
          documentId: unref(documentId),
          sheetId: sid
        },
        data
      })
    } catch { }
  }
}

export const useChangeValueMutation = (
  documentId: Ref<string | null>,
  sheetId: Ref<string>
) => {
  const { client } = useApolloClient()
  const { mutate } = useMutation<
    ChangeValueMutation,
    ChangeValueMutationVariables
  >(changeValueMutation)
  return async (cell: CellType, value: string) => {
    await mutate({
      documentId: unref(documentId),
      sheetId: unref(sheetId),
      cellId: cell.id,
      value
    }, {
      update: (_: DataProxy, result: Omit<FetchResult<ChangeValueMutation>, 'context'>) => {
        if (result.data.changeValue.success) {
          const { values, updatedAt } = result.data.changeValue
          changeSheetValues(values, client, documentId, updatedAt)
        }
      },
      optimisticResponse: {
        __typename: 'Mutation',
        changeValue: {
          __typename: 'ChangeValueMutationPayload',
          success: true,
          errors: null,
          values: [
            {
              id: '',
              sheetId: sheetId.value,
              value,
              error: null,
              columnId: cell.columnId,
              rowId: cell.rowId,
              payload: null,
              __typename: 'ValueType'
            }
          ],
          updatedAt: new Date().toISOString()
        }
      }
    })
  }
}

export function useChangeFileValueMutation (
  documentId: Ref<string | null>,
  sheetId: Ref<string>,
  cell: Ref<CellType>,
  updateSheet: Ref<UpdateType<DocumentSheetQuery>>,
  updateFiles: UpdateType<ValueFilesQuery>
) {
  const { mutate } = useMutation<
    ChangeFileValueMutation,
    ChangeFileValueMutationVariables
  >(changeFileValueMutation)
  return async function (value: string, remainingFiles: string[], newFiles: File[]) {
    await mutate({
      documentId: unref(documentId),
      sheetId: unref(sheetId),
      cellId: unref(cell.value).id,
      value,
      remainingFiles,
      newFiles
    }, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeFileValueMutation>, 'context'>) {
        if (result.data.changeFileValue.success) {
          updateSheet.value(dataProxy, result, (
            data: DocumentSheetQuery, {
              data: { changeFileValue: { value, updatedAt } }
            }: Omit<FetchResult<ChangeFileValueMutation>, 'context'>
          ) => {
            const dataRow = data.documentSheet.rows.find(
              (r: RowDimensionFieldsFragment) => r.id === cell.value.rowId.toString()
            )
            dataRow.updatedAt = updatedAt
            const dataCell = dataRow.cells.find((c: CellFieldsFragment) => c.id === cell.value.id)
            dataCell.value = value
            return data
          })
          updateFiles(dataProxy, result, (
            data: ValueFilesQuery, {
              data: { changeFileValue: { valueFiles } }
            }: Omit<FetchResult<ChangeFileValueMutation>, 'context'>
          ) => {
            data.valueFiles = valueFiles
            return data
          })
        }
      }
    })
  }
}

const updateValues = (data: DocumentSheetQuery, values: ValueType[], updatedAt: string | null = null): void => {
  const rowValues = values.reduce<Record<number, Record<number, ValueType>>>((a, v) => {
    if (!(v.rowId in a)) { a[v.rowId] = {} }
    a[v.rowId][v.columnId] = v
    return a
  }, {})
  for (const [rowId, value] of Object.entries<Record<number, ValueType>>(rowValues)) {
    const row = data.documentSheet.rows.find((r: RowDimensionFieldsFragment) => r.id === rowId)
    if (updatedAt) {
      row.updatedAt = updatedAt
    }
    row.cells = row.cells.map((c: CellFieldsFragment) => {
      if (c.columnId in value) {
        c.value = value[c.columnId].value
        c.error = value[c.columnId].error
      }
      return c
    })
  }
}

export function useUnloadFileValueArchiveMutation (
  documentId: Ref<string | null>,
  sheetId: Ref<string>,
  cell: Ref<CellType>
) {
  const { mutate } = useMutation<
    UnloadFileValueArchiveMutation,
    UnloadFileValueArchiveMutationVariables
  >(unloadFileValueArchiveMutation)
  return async function (): Promise<string> {
    const { columnId, rowId, position } = unref(cell)
    const { data: { unloadFileValueArchive: { src } } } = await mutate({
      documentId: unref(documentId),
      sheetId: unref(sheetId),
      columnId,
      rowId,
      name: position
    })
    return src
  }
}
