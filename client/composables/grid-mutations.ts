import { useMutation } from '@vue/apollo-composable'
import { ApolloClient, DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { Ref, unref } from '#app'
import { UpdateType } from '~/composables/query-common'
import {
  DocumentsSheetQuery,
  DocumentSheetQuery,
  DocumentSheetQueryVariables,
  ValueFilesQuery,
  SheetType,
  RowDimensionType,
  RowDimensionFieldsFragment,
  ColumnDimensionType,
  ColumnDimensionFieldsFragment,
  CellType,
  ValueType,
  CellFieldsFragment,
  GlobalIndicesInputType,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  AddChildRowDimensionMutation,
  AddChildRowDimensionMutationVariables,
  DeleteRowDimensionMutation,
  DeleteRowDimensionMutationVariables,
  DeleteChildRowDimensionMutation,
  DeleteChildRowDimensionMutationVariables,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables,
  ChangeChildRowDimensionHeightMutation,
  ChangeChildRowDimensionHeightMutationVariables,
  ChangeCellDefaultMutation,
  ChangeCellDefaultMutationVariables,
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
import documentSheetQuery from '~/gql/dcis/queries/document_sheet.graphql'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import addChildRowDimensionMutation from '~/gql/dcis/mutations/document/add_child_row_dimension.graphql'
import deleteRowDimensionMutation from '~/gql/dcis/mutations/sheet/delete_row_dimension.graphql'
import deleteChildRowDimensionMutation from '~/gql/dcis/mutations/document/delete_child_row_dimension.graphql'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import changeChildRowDimensionHeightMutation from '~/gql/dcis/mutations/document/change_child_row_dimension_height.graphql'
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
  updateSheet: Ref<UpdateType<DocumentsSheetQuery>>
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
          (data: DocumentsSheetQuery, {
            data: { addRowDimension: { rowDimension } }
          }: Omit<FetchResult<AddRowDimensionMutation>, 'context'>) => {
            data.documentsSheet.rows = addRow(sheet.value.columns, data.documentsSheet.rows, rowDimension)
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
  updateSheet: Ref<UpdateType<DocumentsSheetQuery>>
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
              data: DocumentsSheetQuery, {
                data: { deleteRowDimension: { rowDimensionId } }
              }: Omit<FetchResult<DeleteRowDimensionMutation>, 'context'>
            ) => {
              data.documentsSheet.rows = deleteRow(sheet.value.columns, data.documentsSheet.rows, rowDimensionId)
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

export function useChangeColumnDimensionWidthMutation (updateSheet: Ref<UpdateType<DocumentsSheetQuery>>) {
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
  updateSheet: UpdateType<DocumentsSheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>
) {
  if (result.data.changeColumnDimension.success) {
    updateSheet(
      dataProxy,
      result,
      (
        data: DocumentsSheetQuery,
        { data: { changeColumnDimension } }: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>
      ) => {
        const columnDimension = data.documentsSheet.columns.find((columnDimension: ColumnDimensionFieldsFragment) =>
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

export function useChangeRowDimensionHeightMutation (updateSheet: Ref<UpdateType<DocumentsSheetQuery>>) {
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

export function updateRowDimension (
  updateSheet: UpdateType<DocumentsSheetQuery>,
  dataProxy: DataProxy,
  result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
) {
  if (result.data.changeRowDimension.success) {
    updateSheet(
      dataProxy,
      result,
      (
        data: DocumentsSheetQuery,
        { data: { changeRowDimension } }: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
      ) => {
        const rowDimension = data.documentsSheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
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

export function useChangeCellDefaultMutation (updateSheet: Ref<UpdateType<DocumentsSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeCellDefaultMutation,
    ChangeCellDefaultMutationVariables
  >(changeCellDefaultMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeCellDefaultMutation>, 'context'>) {
      if (result.data.changeCellDefault.success) {
        updateSheet.value(dataProxy, result, (
          data: DocumentsSheetQuery, {
            data: { changeCellDefault }
          }: Omit<FetchResult<ChangeCellDefaultMutation>, 'context'>
        ) => {
          const cell = findCell(
            data.documentsSheet as SheetType,
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

export function useChangeCellsOptionMutation (updateSheet: Ref<UpdateType<DocumentsSheetQuery>>) {
  const { mutate } = useMutation<
    ChangeCellsOptionMutation,
    ChangeCellsOptionMutationVariables
  >(changeCellsOptionMutation, {
    update (dataProxy: DataProxy, result: Omit<FetchResult<ChangeCellsOptionMutation>, 'context'>) {
      if (result.data.changeCellsOption.success) {
        updateSheet.value(dataProxy, result, (
          data: DocumentsSheetQuery, {
            data: { changeCellsOption: { changedOptions } }
          }: Omit<FetchResult<ChangeCellsOptionMutation>, 'context'>
        ) => {
          for (const option of changedOptions) {
            const cell = findCell(
              data.documentsSheet as SheetType,
              (c: CellType) => c.id === option.cellId
            )
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
      cellIds: cells.map((cell: CellType) => cell.id.toString()),
      field,
      value
    })
  }
}

export const useChangeValueMutation = (
  documentId: Ref<string | null>,
  sheetId: Ref<string>,
  cell: Ref<CellType>,
  client: ApolloClient<DocumentSheetQuery>
) => {
  const { mutate } = useMutation<
    ChangeValueMutation,
    ChangeValueMutationVariables
  >(changeValueMutation)
  return async (value: string) => {
    await mutate({
      documentId: unref(documentId),
      sheetId: unref(sheetId),
      cellId: unref(cell.value).id,
      value
    }, {
      update: (_: DataProxy, result: Omit<FetchResult<ChangeValueMutation>, 'context'>) => {
        if (result.data.changeValue.success) {
          const { values, updatedAt } = result.data.changeValue
          const sheetValue = values.reduce<Record<number, ValueType[]>>((a, v) => {
            if (!(v.sheetId in a)) { a[v.sheetId] = [] }
            a[v.sheetId].push(v)
            return a
          }, {})
          // Читаем все sheet для которых пришли ответные данные изменение ячеек
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
              verified: true,
              columnId: cell.value.columnId,
              rowId: cell.value.rowId,
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

/**
 *
 * @param data
 * @param values
 * @param updatedAt
 */
const updateValues = (data: DocumentSheetQuery, values: ValueType[], updatedAt: string): void => {
  const rowValues = values.reduce<Record<number, Record<number, ValueType>>>((a, v) => {
    if (!(v.rowId in a)) { a[v.rowId] = {} }
    a[v.rowId][v.columnId] = v
    return a
  }, {})
  for (const [rowId, value] of Object.entries<Record<number, ValueType>>(rowValues)) {
    const row = data.documentSheet.rows.find((r: RowDimensionFieldsFragment) => r.id === rowId)
    row.updatedAt = updatedAt
    row.cells = row.cells.map((c: CellFieldsFragment) => {
      if (c.columnId in value) {
        c.value = value[c.columnId].value
        c.verified = value[c.columnId].verified
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
