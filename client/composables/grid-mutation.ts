import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { Ref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  RowDimensionFieldsFragment,
  SheetQuery,
  GlobalIndicesInputType,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables
} from '~/types/graphql'
import { BuildRowType } from '~/types/grid'
import { parsePosition } from '~/services/grid'
import addRodDimension from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'

export enum AddRowDimensionPosition {
  BEFORE,
  AFTER,
  INSIDE
}

export function useAddRowDimensionMutation (
  rows: Ref<BuildRowType[]>,
  sheetId: Ref<string>,
  documentId: Ref<string | null>,
  updateSheet: UpdateType<SheetQuery>
) {
  const { mutate } = useMutation<AddRowDimensionMutation, AddRowDimensionMutationVariables>(addRodDimension)
  return async function (buildRow: BuildRowType, position: AddRowDimensionPosition) {
    const rowDimension = buildRow.rowDimension
    let variables: AddRowDimensionMutationVariables | Omit<
      AddRowDimensionMutationVariables, 'index' | 'globalIndex'
    > = {
      sheetId: sheetId.value,
      documentId: documentId.value,
      parentId: rowDimension.parent?.id,
      globalIndices: collectGlobalIndices(rows.value, buildRow)
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
  rows: BuildRowType[],
  row: BuildRowType | null | undefined,
  globalIndices: GlobalIndicesInputType[] | null = null
): GlobalIndicesInputType[] {
  globalIndices = globalIndices || []
  if (!row) {
    return globalIndices
  }
  return collectGlobalIndices(
    rows,
    rows.find((buildRow: BuildRowType) => buildRow.rowDimension.id === row.rowDimension.parent?.id),
    [...globalIndices, { rowId: row.rowDimension.id, globalIndex: row.rowDimension.globalIndex }]
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
