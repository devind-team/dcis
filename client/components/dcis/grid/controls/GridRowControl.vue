<template lang="pug">
  v-menu(bottom close-on-content-click)
    template(#activator="{ on: onMenu }")
      v-tooltip(right open-delay="1000")
        template(#activator="{ on: onTooltip, attrs }")
          div(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs") {{ row.index }}
        span Дата изменения: {{ dateTimeHM(row.dimension.updatedAt) }}
    v-list
      v-list-item(@click="addRowDimension(+row.id, 'before')")
        v-list-item-icon
          v-icon mdi-table-row-plus-before
        v-list-item-content Добавить строку выше
      v-list-item(@click="addRowDimension(+row.id, 'after')")
        v-list-item-icon
          v-icon mdi-table-row-plus-after
        v-list-item-content Добавить строку ниже
      v-list-item(@click="deleteRowDimension(+row.id)")
        v-list-item-icon
          v-icon(color="error") mdi-delete
        v-list-item-content(color="error") Удалить строку
</template>

<script lang="ts">
import { ApolloCache, DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import type { PropType } from '#app'
import { defineComponent, inject } from '#app'
import { BuildRowType } from '~/types/grid-types'
import {
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  DeleteRowDimensionMutation, DeleteRowDimensionMutationVariables,
  DocumentQuery, RowDimensionType
} from '~/types/graphql'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import deleteRowDimensionMutation from '~/gql/dcis/mutations/sheet/delete_row_dimension.graphql'
import { useFilters } from '~/composables'

export type AddRowDimensionMutationResult = { data: AddRowDimensionMutation }
export type DeleteRowDimensionMutationResult = { data: DeleteRowDimensionMutation }

type DocumentUpdateType<T> = (
  cache: ApolloCache<DocumentQuery | any> | any,
  result: T,
  transform: (dc: any, r: T) => any
) => DataProxy

export default defineComponent({
  props: {
    row: { type: Object as PropType<BuildRowType>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()
    const documentId: string = inject<string>('documentId')
    const documentUpdate: DocumentUpdateType<any> = inject<DocumentUpdateType<any>>('documentUpdate')
    const addRowDimension = (rowId: number, position: 'before' | 'after') => {
      const { mutate } = useMutation<AddRowDimensionMutation, AddRowDimensionMutationVariables>(addRowDimensionMutation, {
        update: (cache, result) => documentUpdate(
          cache,
          result,
          (dataCache: DocumentQuery, { data: { addRowDimension: { success, rowDimension, cells, mergedCells } } }: AddRowDimensionMutationResult) => {
            if (success) {
              dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId).cells.push(...cells)
              const rows: RowDimensionType[] = dataCache.document.sheets
                .find(sh => sh.id === props.row.sheetId)
                .rows
                .map((r: RowDimensionType | any) => (
                  r.index >= rowDimension.index ? Object.assign(r, { index: r.index + 1 }) : r)
                )
              rows.splice(rowDimension.index - 1, 0, rowDimension as RowDimensionType)
              dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId).rows = rows as any
              dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId).mergedCells = mergedCells
            }
            return dataCache
          }
        )
      })
      mutate({ documentId, rowId, position })
    }

    const deleteRowDimension = (rowId: number) => {
      const { mutate } = useMutation<DeleteRowDimensionMutation, DeleteRowDimensionMutationVariables>(
        deleteRowDimensionMutation, {
          update: (cache, result) => documentUpdate(
            cache,
            result,
            (dataCache: DocumentQuery, { data: { deleteRowDimension: { success, rowId, index, mergedCells } } }: DeleteRowDimensionMutationResult) => {
              if (success) {
                const rows: RowDimensionType[] = dataCache.document.sheets
                  .find(sheet => sheet.id === props.row.sheetId)
                  .rows
                  .filter((r: RowDimensionType | any) => Number(r.id) !== rowId)
                  .map((r: RowDimensionType | any) => (
                    r.index > index ? Object.assign(r, { index: r.index - 1 }) : r
                  ))
                dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId).rows = rows as any
                dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId).mergedCells = mergedCells
              }
              return dataCache
            }
          )
        }
      )
      mutate({ rowId })
    }
    return { addRowDimension, deleteRowDimension, dateTimeHM }
  }
})
</script>
