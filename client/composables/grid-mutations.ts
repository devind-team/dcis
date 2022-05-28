import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { Ref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  SheetQuery,
  ValueFilesQuery,
  SheetType,
  RowDimensionType,
  RowDimensionFieldsFragment,
  ColumnDimensionType,
  ColumnDimensionFieldsFragment,
  CellType,
  CellFieldsFragment,
  GlobalIndicesInputType,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables,
  ChangeCellsOptionMutation,
  ChangeCellsOptionMutationVariables,
  ChangeValueMutation,
  ChangeValueMutationVariables,
  ChangeFileValueMutation,
  ChangeFileValueMutationVariables, ValueFilesQueryVariables
} from '~/types/graphql'
import { parsePosition, findCell } from '~/services/grid'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import changeCellsOptionMutation from '~/gql/dcis/mutations/sheet/change_cells_option.graphql'
import changeValueMutation from '~/gql/dcis/mutations/sheet/change_value.graphql'
import changeFileValueMutation from '~/gql/dcis/mutations/sheet/change_file_value.graphql'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'

export enum AddRowDimensionPosition {
  BEFORE,
  AFTER,
  INSIDE
}

export function useAddRowDimensionMutation (
  rows: Ref<RowDimensionType[]>,
  sheetId: Ref<string>,
  documentId: Ref<string | null>,
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
      documentId: documentId.value,
      parentId: rowDimension.parent?.id,
      globalIndices: collectGlobalIndices(rows.value, rowDimension)
    }
    if (position === AddRowDimensionPosition.AFTER) {
      variables = { ...variables, index: rowDimension.index + 1, globalIndex: rowDimension.globalIndex + 1 }
    } else if (position === AddRowDimensionPosition.BEFORE) {
      variables = { ...variables, index: rowDimension.index, globalIndex: rowDimension.globalIndex }
    } else if (position === AddRowDimensionPosition.INSIDE) {
      const childGlobalIndex = rowDimension.children.length ? rowDimension.children.at(-1).index + 1 : 1
      variables = {
        ...variables,
        parentId: rowDimension.id,
        index: rowDimension.children.length ? rowDimension.children.at(-1).index + 1 : 1,
        globalIndex: rowDimension.globalIndex + childGlobalIndex
      }
    }
    await mutate(variables as AddRowDimensionMutationVariables)
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
    rows.find((row: RowDimensionType) => row.id === row.parent?.id),
    [...globalIndices, { rowId: row.id, globalIndex: row.globalIndex }]
  )
}

function addRow (rows: RowDimensionFieldsFragment[], newRow: RowDimensionFieldsFragment): RowDimensionFieldsFragment[] {
  const newRows: RowDimensionFieldsFragment[] = []
  for (const row of rows) {
    if (row.globalIndex === newRow.globalIndex) {
      newRows.push(newRow)
    }
    if (row.globalIndex < newRow.globalIndex) {
      newRows.push(row)
    } else if (row.globalIndex >= newRow.globalIndex) {
      row.globalIndex += 1
      if (row.index >= newRow.index && row.parent?.id === newRow.parent?.id) {
        row.index += 1
      }
      row.name = getRowName(rows, row)
      updateCellsPositions(row)
      newRows.push(row)
    }
  }
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

function updateCellsPositions (row: RowDimensionFieldsFragment): void {
  for (const cell of row.cells) {
    const { column } = parsePosition(cell.globalPosition)
    cell.position = `${column}${row.name}`
    cell.globalPosition = `${column}${row.globalIndex}`
    cell.relatedGlobalPositions = cell.relatedGlobalPositions.map((position: string) => {
      const parsedPosition = parsePosition(position)
      return `${parsedPosition.column}${parsedPosition.row + 1}`
    })
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
  sheetId: Ref<string>,
  documentId: Ref<string | null>,
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
  sheetId: Ref<string>,
  documentId: Ref<string | null>,
  updateSheet: Ref<UpdateType<SheetQuery>>
) {
  const { mutate } = useMutation<
    ChangeValueMutation,
    ChangeValueMutationVariables
  >(changeValueMutation)
  return async function (cell: CellType, value: string) {
    await mutate({
      documentId: documentId.value,
      sheetId: sheetId.value,
      columnId: cell.columnId,
      rowId: cell.rowId,
      value
    }, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeValueMutation>, 'context'>) {
        if (result.data.changeValue.success) {
          updateSheet.value(dataProxy, result, (
            data: SheetQuery, {
              data: { changeValue: { value, updatedAt } }
            }: Omit<FetchResult<ChangeValueMutation>, 'context'>
          ) => {
            const dataRow = data.sheet.rows.find((r: RowDimensionFieldsFragment) => r.id === cell.rowId)
            dataRow.updatedAt = updatedAt
            const dataCell = dataRow.cells.find((c: CellFieldsFragment) => c.id === cell.id)
            dataCell.value = value
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
  sheetId: Ref<string>,
  documentId: Ref<string | null>,
  updateSheet: Ref<UpdateType<SheetQuery>>,
  updateFiles: UpdateType<ValueFilesQuery>
) {
  const { mutate } = useMutation<
    ChangeFileValueMutation,
    ChangeFileValueMutationVariables
  >(changeFileValueMutation)
  return async function (cell: CellType, value: string, remainingFiles: string[], newFiles: File[]) {
    await mutate({
      documentId: documentId.value,
      sheetId: sheetId.value,
      columnId: cell.columnId,
      rowId: cell.rowId,
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
            const dataRow = data.sheet.rows.find((r: RowDimensionFieldsFragment) => r.id === cell.rowId)
            dataRow.updatedAt = updatedAt
            const dataCell = dataRow.cells.find((c: CellFieldsFragment) => c.id === cell.id)
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
