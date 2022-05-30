import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { Ref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  SheetQuery,
  ValueFilesQuery,
  ValueFilesQueryVariables,
  SheetType,
  RowDimensionType,
  RowDimensionFieldsFragment,
  ColumnDimensionType,
  ColumnDimensionFieldsFragment,
  CellType,
  CellFieldsFragment,
  GlobalIndicesInputType,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  DeleteRowDimensionMutation,
  DeleteRowDimensionMutationVariables,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables,
  ChangeCellsOptionMutation,
  ChangeCellsOptionMutationVariables,
  ChangeValueMutation,
  ChangeValueMutationVariables,
  ChangeFileValueMutation,
  ChangeFileValueMutationVariables,
  UnloadFileValueArchiveMutation,
  UnloadFileValueArchiveMutationVariables
} from '~/types/graphql'
import { parsePosition, findCell } from '~/services/grid'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import deleteRowDimensionMutation from '~/gql/dcis/mutations/sheet/delete_row_dimension.graphql'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import changeCellsOptionMutation from '~/gql/dcis/mutations/sheet/change_cells_option.graphql'
import changeValueMutation from '~/gql/dcis/mutations/sheet/change_value.graphql'
import changeFileValueMutation from '~/gql/dcis/mutations/sheet/change_file_value.graphql'
import unloadFileValueArchiveMutation from '~/gql/dcis/mutations/sheet/unload_file_value_archive.graphql'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'

export enum AddRowDimensionPosition {
  BEFORE,
  AFTER,
  INSIDE
}

export function useAddRowDimensionMutation (
  documentId: Ref<string | null>,
  sheetId: Ref<string>,
  rows: Ref<RowDimensionType[]>,
  updateSheet: Ref<UpdateType<SheetQuery>>
) {
  const { mutate } = useMutation<AddRowDimensionMutation, AddRowDimensionMutationVariables>(addRowDimensionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) {
      if (result.data.addRowDimension.success) {
        updateSheet.value(
          dataProxy,
          result,
          (data: SheetQuery, {
            data: { addRowDimension: { rowDimension } }
          }: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) => {
            data.sheet.rows = addRow(data.sheet.rows, rowDimension)
            return data
          })
      }
    }
  })
  return async function (rowDimension: RowDimensionType, position: AddRowDimensionPosition) {
    let variables: AddRowDimensionMutationVariables | Omit<
      AddRowDimensionMutationVariables, 'index' | 'globalIndex'
    > = {
      sheetId: sheetId.value,
      documentId: rowDimension.parent ? documentId.value : null,
      parentId: rowDimension.parent?.id,
      globalIndices: collectGlobalIndices(rows.value, rowDimension)
    }
    if (position === AddRowDimensionPosition.AFTER) {
      variables = { ...variables, index: rowDimension.index + 1, globalIndex: rowDimension.globalIndex + 1 }
    } else if (position === AddRowDimensionPosition.BEFORE) {
      variables = { ...variables, index: rowDimension.index, globalIndex: rowDimension.globalIndex }
    } else if (position === AddRowDimensionPosition.INSIDE) {
      const index = rowDimension.children.length ? rowDimension.children.at(-1).index + 1 : 1
      variables = {
        ...variables,
        documentId: documentId.value,
        parentId: rowDimension.id,
        index,
        globalIndex: rowDimension.globalIndex + index
      }
    }
    await mutate(variables as AddRowDimensionMutationVariables)
  }
}

export function useDeleteRowDimensionMutation (updateSheet: Ref<UpdateType<SheetQuery>>) {
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
              data: SheetQuery, {
                data: { deleteRowDimension: { rowDimensionId } }
              }: Omit<FetchResult<DeleteRowDimensionMutation>, 'context'>
            ) => {
              data.sheet.rows = deleteRow(data.sheet.rows, rowDimensionId)
              return data
            })
        }
      }
    })
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

function addRow (
  rows: RowDimensionFieldsFragment[],
  newRow: RowDimensionFieldsFragment
): RowDimensionFieldsFragment[] {
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
  rows: RowDimensionFieldsFragment[],
  deletedRowId: string
): RowDimensionFieldsFragment[] {
  const newRows: RowDimensionFieldsFragment[] = []
  let deletedRow: RowDimensionFieldsFragment | null = null
  for (const row of rows) {
    if (row.id === deletedRowId) {
      deletedRow = row
      continue
    }
    if (!deletedRow) {
      newRows.push(row)
    } else {
      row.globalIndex -= 1
      if (row.index >= deletedRow.index && row.parent?.id === deletedRow.parent?.id) {
        row.index -= 1
      }
      row.name = getRowName(rows, row)
      updateCellsPositions(row, (index: number) => index - 1)
      newRows.push(row)
    }
  }
  updateRelativeRows(newRows)
  return newRows
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
    for (const child of row.children) {
      const sourceChild = rows.find((r: RowDimensionFieldsFragment) => r.id === child.id)
      child.index = sourceChild.index
      child.globalIndex = sourceChild.globalIndex
    }
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

export function useChangeColumnDimensionWidthMutation (updateSheet: Ref<UpdateType<SheetQuery>>) {
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
      fixed: columnDimension.fixed,
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
          ...variables,
          updatedAt: new Date().toISOString()
        }
      }
    })
  }
}

export function updateColumnDimension (
  updateSheet: UpdateType<SheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>
) {
  if (result.data.changeColumnDimension.success) {
    updateSheet(
      dataProxy,
      result,
      (
        data: SheetQuery,
        { data: { changeColumnDimension } }: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>
      ) => {
        const columnDimension = data.sheet.columns.find((columnDimension: ColumnDimensionFieldsFragment) =>
          columnDimension.id === changeColumnDimension.columnDimensionId)!
        columnDimension.width = changeColumnDimension.width
        columnDimension.fixed = changeColumnDimension.fixed
        columnDimension.hidden = changeColumnDimension.hidden
        columnDimension.updatedAt = changeColumnDimension.updatedAt
        return data
      }
    )
  }
}

export function useChangeRowDimensionHeightMutation (updateSheet: Ref<UpdateType<SheetQuery>>) {
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
      fixed: rowDimension.fixed,
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
          ...variables,
          updatedAt: new Date().toISOString()
        }
      }
    })
  }
}

export function updateRowDimension (
  updateSheet: UpdateType<SheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
) {
  if (result.data.changeRowDimension.success) {
    updateSheet(
      dataProxy,
      result,
      (
        data: SheetQuery,
        { data: { changeRowDimension } }: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
      ) => {
        const rowDimension = data.sheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
          rowDimension.id === changeRowDimension.rowDimensionId)!
        rowDimension.height = changeRowDimension.height
        rowDimension.fixed = changeRowDimension.fixed
        rowDimension.hidden = changeRowDimension.hidden
        rowDimension.dynamic = changeRowDimension.dynamic
        rowDimension.updatedAt = changeRowDimension.updatedAt
        return data
      }
    )
  }
}

export function useChangeCellsOptionMutation (
  documentId: Ref<string | null>,
  sheetId: Ref<string>,
  updateSheet: Ref<UpdateType<SheetQuery>>
) {
  const { mutate } = useMutation<
    ChangeCellsOptionMutation,
    ChangeCellsOptionMutationVariables
  >(changeCellsOptionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeCellsOptionMutation>, 'context'>) {
      if (result.data.changeCellsOption.success) {
        updateSheet.value(dataProxy, result, (
          data: SheetQuery, {
            data: { changeCellsOption: { changedOptions } }
          }: Omit<FetchResult<ChangeCellsOptionMutation>, 'context'>
        ) => {
          for (const option of changedOptions) {
            const cell = findCell(data.sheet as SheetType, (c: CellType) => c.id === option.cellId)
            if (cell.kind === 'fl' && option.field === 'kind' && option.value !== 'fl') {
              try {
                const variables: ValueFilesQueryVariables = {
                  sheetId: sheetId.value,
                  documentId: documentId.value,
                  columnId: cell.columnId,
                  rowId: cell.rowId
                }
                dataProxy.readQuery<ValueFilesQuery, ValueFilesQueryVariables>({
                  query: valueFilesQuery,
                  variables
                })
                dataProxy.writeQuery<ValueFilesQuery, ValueFilesQueryVariables>({
                  data: { valueFiles: [] },
                  query: valueFilesQuery,
                  variables
                })
              } catch (_) {}
            }
            if (option.field === 'size') {
              cell[option.field] = Number(option.value)
            } else if (['strong', 'italic', 'strike'].includes(option.field)) {
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
      cellIds: cells.map((cell: CellType) => cell.id),
      field,
      value
    })
  }
}

export function useChangeValueMutation (
  documentId: Ref<string | null>,
  sheetId: Ref<string>,
  cell: Ref<CellType>,
  updateSheet: Ref<UpdateType<SheetQuery>>
) {
  const { mutate } = useMutation<
    ChangeValueMutation,
    ChangeValueMutationVariables
  >(changeValueMutation)
  return async function (value: string) {
    await mutate({
      documentId: documentId.value,
      sheetId: sheetId.value,
      columnId: cell.value.columnId,
      rowId: cell.value.rowId,
      value
    }, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeValueMutation>, 'context'>) {
        if (result.data.changeValue.success) {
          updateSheet.value(dataProxy, result, (
            data: SheetQuery, {
              data: { changeValue: { value, updatedAt } }
            }: Omit<FetchResult<ChangeValueMutation>, 'context'>
          ) => {
            updateCellValue(data, cell.value, updatedAt, value)
            return data
          })
        }
      },
      optimisticResponse: {
        __typename: 'Mutation',
        changeValue: {
          __typename: 'ChangeValueMutationPayload',
          success: true,
          errors: [],
          value,
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
  updateSheet: Ref<UpdateType<SheetQuery>>,
  updateFiles: UpdateType<ValueFilesQuery>
) {
  const { mutate } = useMutation<
    ChangeFileValueMutation,
    ChangeFileValueMutationVariables
  >(changeFileValueMutation)
  return async function (value: string, remainingFiles: string[], newFiles: File[]) {
    await mutate({
      documentId: documentId.value,
      sheetId: sheetId.value,
      columnId: cell.value.columnId,
      rowId: cell.value.rowId,
      value,
      remainingFiles,
      newFiles
    }, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeFileValueMutation>, 'context'>) {
        if (result.data.changeFileValue.success) {
          updateSheet.value(dataProxy, result, (
            data: SheetQuery, {
              data: { changeFileValue: { value, updatedAt } }
            }: Omit<FetchResult<ChangeFileValueMutation>, 'context'>
          ) => {
            updateCellValue(data, cell.value, updatedAt, value)
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

function updateCellValue (data: SheetQuery, cell: CellType, updatedAt: string, value: string): void {
  const dataRow = data.sheet.rows.find((r: RowDimensionFieldsFragment) => r.id === cell.rowId)
  dataRow.updatedAt = updatedAt
  const dataCell = dataRow.cells.find((c: CellFieldsFragment) => c.id === cell.id)
  dataCell.value = value
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
    const { data: { unloadFileValueArchive: { src } } } = await mutate({
      documentId: documentId.value,
      sheetId: sheetId.value,
      columnId: cell.value.columnId,
      rowId: cell.value.rowId,
      name: cell.value.position
    })
    return src
  }
}
