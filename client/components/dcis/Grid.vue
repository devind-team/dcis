<template lang="pug">
  table.grid__table
    thead
      tr
        td.header-cell
        td(
          v-for="buildColumn in columns"
          :key="buildColumn.dimension.id"
          :style="buildColumn.style"
        ).header-cell {{ buildColumn.positional }}
    tbody
      tr(
        v-for="row in rows"
        :key="row.dimension.id"
        :style="row.style"
      )
        td.header-cell
          v-menu(bottom close-on-content-click)
            template(#activator="{ on, attrs }")
              div(v-on="on" v-bind="attrs") {{ row.index }}
            v-list
              v-list-item(@click="addRowDimension(+row.dimension.id, 'before')")
                v-list-item-icon
                  v-icon mdi-table-row-plus-before
                v-list-item-content Добавить строку выше
              v-list-item(@click="addRowDimension(+row.dimension.id, 'after')")
                v-list-item-icon
                  v-icon mdi-table-row-plus-after
                v-list-item-content Добавить строку ниже
              v-list-item(@click="deleteRowDimension(+row.dimension.id)")
                v-list-item-icon
                  v-icon(color="error") mdi-delete
                v-list-item-content(color="error") Удалить строку
        td(
          v-for="cell in row.cells"
          :key="cell.cell.id"
          :colspan="cell.colspan"
          :rowspan="cell.rowspan"
          :class="{marked: active === cell.position}"
          :style="cell.style"
          @click="setActive(cell.position)"
          @dblclick="setActive(cell.position, true)"
        )
          input(
            v-if="active === cell.position"
            v-focus
            :value="cell.value"
            @keyup.enter="changeValue(cell.cell.columnId, cell.cell.rowId, $event.target.value)"
            style="width: 100%; min-width:100px;"
          )
          template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { PropType, Ref } from '#app'
import { defineComponent, inject, toRef } from '#app'
import {
  AddRowDimensionMutation,
  AddRowDimensionMutationVariables,
  ChangeValueMutation,
  ChangeValueMutationVariables,
  DeleteRowDimensionMutation, DeleteRowDimensionMutationVariables,
  DocumentQuery, RowDimensionType,
  SheetType,
  ValueType
} from '~/types/graphql'
import { useGrid } from '~/composables/grid'
import changeValueMutation from '~/gql/dcis/mutations/document/change_value.graphql'
import addRowDimensionMutation from '~/gql/dcis/mutations/sheet/add_row_dimension.graphql'
import deleteRowDimensionMutation from '~/gql/dcis/mutations/sheet/delete_row_dimension.graphql'
import row from "vuetify/src/components/VDataTable/Row";

export type ChangeValueMutationResult = { data: ChangeValueMutation }
export type AddRowDimensionMutationResult = { data: AddRowDimensionMutation }
export type DeleteRowDimensionMutationResult = { data: DeleteRowDimensionMutation }

export default defineComponent({
  directives: {
    focus: {
      inserted (el) {
        el.focus()
      }
    }
  },
  props: {
    documentId: { type: String, required: true },
    sheet: { type: Object as PropType<SheetType>, required: true }
  },
  setup (props) {
    const sheet: Ref<SheetType> = toRef(props, 'sheet')
    const {
      columns,
      rows,
      mergeCells,
      mergedCells,
      active,
      setActive
    } = useGrid(sheet)

    const documentUpdate: any = inject('documentUpdate')

    const addRowDimension = (rowId: number, position: 'after' | 'before') => {
      const { mutate } = useMutation<AddRowDimensionMutation, AddRowDimensionMutationVariables>(addRowDimensionMutation, {
        update: (cache, result) => documentUpdate(
          cache,
          result,
          (dataCache: DocumentQuery, { data: { addRowDimension: { success, rowDimension, cells } } }: AddRowDimensionMutationResult) => {
            if (success) {
              dataCache.document.sheets.find(sheet => sheet.id === props.sheet.id).cells.push(...cells)
              const rows: RowDimensionType[] = dataCache.document.sheets
                .find(sh => sh.id === props.sheet.id)
                .rows
                .map((r: RowDimensionType | any) => (
                  r.index >= rowDimension.index ? Object.assign(r, { index: r.index + 1 }) : r)
                )
              rows.splice(rowDimension.index - 1, 0, rowDimension as RowDimensionType)
              dataCache.document.sheets.find(sheet => sheet.id === props.sheet.id).rows = rows as any
            }
            return dataCache
          }
        )
      })
      mutate({ documentId: props.documentId, rowId, position })
    }

    const deleteRowDimension = (rowId: number) => {
      const { mutate } = useMutation<DeleteRowDimensionMutation, DeleteRowDimensionMutationVariables>(
        deleteRowDimensionMutation, {
          update: (cache, result) => documentUpdate(
            cache,
            result,
            (dataCache: DocumentQuery, { data: { deleteRowDimension: { success, rowId, index } } }: DeleteRowDimensionMutationResult) => {
              if (success) {
                console.log(rowId, index)
                const rows: RowDimensionType[] = dataCache.document.sheets
                  .find(sheet => sheet.id === props.sheet.id)
                  .rows
                  .filter((r: RowDimensionType | any) => Number(r.id) !== rowId)
                  .map((r: RowDimensionType | any) => (
                    r.index > index ? Object.assign(r, { index: r.index - 1 }) : r
                  ))
                dataCache.document.sheets.find(sheet => sheet.id === props.sheet.id).rows = rows as any
              }
              return dataCache
            }
          )
        }
      )
      mutate({ rowId })
    }

    const { mutate: changeValueMutate } = useMutation<ChangeValueMutation, ChangeValueMutationVariables>(changeValueMutation, {
      update: (cache, result) => documentUpdate(
        cache,
        result,
        (dataCache: DocumentQuery, { data: { changeValue: { success, value } } }: ChangeValueMutationResult) => {
          if (success) {
            const values: ValueType[] = dataCache.document.sheets!
              .find(sh => sh.id === props.sheet.id)
              .values.filter((v: ValueType) => v.id !== value.id)
            dataCache.document.sheets!.find(sh => sh.id === props.sheet.id)!.values = [...values, value] as any
            setActive(null)
          }
          return dataCache
        })
    })

    const changeValue = (columnId: number, rowId: number, value: string) => {
      changeValueMutate({
        documentId: props.documentId,
        sheetId: +props.sheet.id,
        columnId,
        rowId,
        value
      })
    }
    return { columns, rows, mergedCells, mergeCells, active, setActive, addRowDimension, deleteRowDimension, changeValue }
  }
})
</script>

<style lang="sass">
.grid__table
  tr td
    box-sizing: border-box
    &.marked
      border: 2px solid blue
  border-collapse: collapse
  user-select: none
  .header-cell
    text-align: center
    background: lightgrey
    cursor: pointer
  .active-cell
    border: 2px solid blue
  .input
    width: 100%
    height: 100%
    outline: none
  thead
    td
      height: 35px
      border: 1px solid grey
  tbody
    .header-cell
      width: 30px
    td
      border: 1px solid grey
</style>
