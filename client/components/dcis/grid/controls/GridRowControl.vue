<template lang="pug">
  v-menu(bottom close-on-content-click)
    template(#activator="{ on: onMenu }")
      v-tooltip(right open-delay="1000")
        template(#activator="{ on: onTooltip, attrs }")
          div(
            v-bind="attrs"
            v-on="onTooltip"
            @contextmenu.prevent="onMenu.click"
            :class="contentClass"
          ) {{ row.index }}
        span {{ t('dcis.grid.rowControl.updatedAt', { updatedAt: dateTimeHM(row.dimension.updatedAt) } ) }}
    v-list(dense)
      v-list-item
        v-list-item-icon
          v-icon mdi-cog
        v-list-item-content {{ t('dcis.grid.rowControl.properties') }}
      v-list-item(@click="addRowDimension(+row.id, 'before')")
        v-list-item-icon
          v-icon mdi-table-row-plus-before
        v-list-item-content {{ t('dcis.grid.rowControl.addRowAbove') }}
      v-list-item(@click="addRowDimension(+row.id, 'after')")
        v-list-item-icon
          v-icon mdi-table-row-plus-after
        v-list-item-content {{ t('dcis.grid.rowControl.addRowBelow') }}
      v-list-item(v-if="row.dynamic")
        v-list-item-icon
          v-icon
        v-list-item-content {{ t('dcis.grid.rowControl.addChildRow') }}
      v-list-item(@click="deleteRowDimension(+row.id)")
        v-list-item-icon
          v-icon(color="error") mdi-delete
        v-list-item-content(color="error") {{ t('dcis.grid.rowControl.deleteRow') }}
</template>

<script lang="ts">
import { ApolloCache, DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import type { PropType } from '#app'
import type { BuildRowType } from '~/types/grid-types'
import type {
  RowDimensionFieldsFragment,
  CellType,
  ValueType,
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  DeleteRowDimensionMutation,
  DeleteRowDimensionMutationVariables,
  DocumentQuery
} from '~/types/graphql'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import deleteRowDimensionMutation from '~/gql/dcis/mutations/sheet/delete_row_dimension.graphql'

export type AddRowDimensionMutationResult = { data: AddRowDimensionMutation }
export type DeleteRowDimensionMutationResult = { data: DeleteRowDimensionMutation }

type DocumentUpdateType<T> = (
  cache: ApolloCache<DocumentQuery | any> | any,
  result: T,
  transform: (dc: any, r: T) => any
) => DataProxy

export default defineComponent({
  props: {
    row: { type: Object as PropType<BuildRowType>, required: true },
    contentClass: { type: Array as PropType<(string | Record<string, boolean>)[]>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { dateTimeHM } = useFilters()
    const documentId: string = inject<string>('documentId')
    const documentUpdate: DocumentUpdateType<any> = inject<DocumentUpdateType<any>>('documentUpdate')
    const addRowDimension = (rowId: number, position: 'before' | 'after') => {
      const { mutate } = useMutation<
        AddRowDimensionMutation,
        AddRowDimensionMutationVariables
      >(addRowDimensionMutation, {
        update: (cache, result) => documentUpdate(
          cache,
          result,
          (
            dataCache: DocumentQuery, {
              data: { addRowDimension: { success, rowDimension, cells, mergedCells } }
            }: AddRowDimensionMutationResult
          ) => {
            if (success) {
              const sheet = dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId)
              sheet.cells.push(...cells)
              const rows = sheet.rows
                .map((r: RowDimensionFieldsFragment) => (
                  r.index >= rowDimension.index ? Object.assign(r, { index: r.index + 1 }) : r)
                )
              rows.splice(rowDimension.index - 1, 0, rowDimension)
              sheet.rows = rows
              sheet.mergedCells = mergedCells
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
            (
              dataCache: DocumentQuery, {
                data: { deleteRowDimension: { success, rowId, index, mergedCells } }
              }: DeleteRowDimensionMutationResult
            ) => {
              if (success) {
                const sheet = dataCache.document.sheets.find(sheet => sheet.id === props.row.sheetId)
                sheet.rows = sheet.rows
                  .filter((r: RowDimensionFieldsFragment) => Number(r.id) !== rowId)
                  .map((r: RowDimensionFieldsFragment) => (
                    r.index > index ? Object.assign(r, { index: r.index - 1 }) : r
                  ))
                sheet.cells = sheet.cells.filter((c: CellType) => c.rowId !== rowId)
                sheet.values = sheet.values.filter((v: ValueType) => v.rowId !== rowId)
                sheet.mergedCells = mergedCells
              }
              return dataCache
            }
          )
        }
      )
      mutate({ rowId })
    }
    return { t, addRowDimension, deleteRowDimension, dateTimeHM }
  }
})
</script>
