import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { Ref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  SheetQuery,
  RowDimensionType,
  RowDimensionFieldsFragment,
  GlobalIndicesInputType,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables
} from '~/types/graphql'
import { parsePosition } from '~/services/grid'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'

export enum AddRowDimensionPosition {
  BEFORE,
  AFTER,
  INSIDE
}

export function useAddRowDimensionMutation (
  rows: Ref<RowDimensionType[]>,
  sheetId: Ref<string>,
  documentId: Ref<string | null>,
  updateSheet: UpdateType<SheetQuery>
) {
  const { mutate } = useMutation<AddRowDimensionMutation, AddRowDimensionMutationVariables>(addRowDimensionMutation)
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
    await mutate(variables as AddRowDimensionMutationVariables, {
      update (dataProxy: DataProxy, result: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) {
        updateSheet(
          dataProxy,
          result,
          (data: SheetQuery, {
            data: {
              addRowDimension: {
                success, rowDimension
              }
            }
          }: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) => {
            if (success) {
              data.sheet.rows = addRow(data.sheet.rows, rowDimension)
            }
            return data
          })
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

export function useChangeRowDimensionHeightMutation (updateSheet: UpdateType<SheetQuery>) {
  const { mutate } = useMutation<
    ChangeRowDimensionMutation,
    ChangeRowDimensionMutationVariables
  >(changeRowDimensionMutation)
  return async function (rowDimension: RowDimensionType, height: number) {
    const variables = {
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
          ...variables
        }
      },
      update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>) {
        updateRowDimension(updateSheet, dataProxy, result)
      }
    })
  }
}

export function updateRowDimension (
  updateSheet: UpdateType<SheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
) {
  updateSheet(
    dataProxy,
    result,
    (
      data: SheetQuery,
      { data: { changeRowDimension } }: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
    ) => {
      if (changeRowDimension.success) {
        const rowDimension = data.sheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
          rowDimension.id === changeRowDimension.rowDimensionId)!
        rowDimension.height = changeRowDimension.height
        rowDimension.fixed = changeRowDimension.fixed
        rowDimension.hidden = changeRowDimension.hidden
        rowDimension.dynamic = changeRowDimension.dynamic
      }
      return data
    }
  )
}
