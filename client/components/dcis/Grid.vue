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
        td.header-cell {{ row.index }}
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
import { defineComponent, inject, toRef} from '#app'
import {ChangeValueMutation, ChangeValueMutationVariables, DocumentQuery, SheetType, ValueType} from '~/types/graphql'
import { useGrid } from '~/composables/grid'
import changeValueMutation from '~/gql/dcis/mutations/document/change_value.graphql'

export type ChangeValueMutationResult = { data: ChangeValueMutation }

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

    const { mutate: changeValueMutate } = useMutation<ChangeValueMutation, ChangeValueMutationVariables>(changeValueMutation, {
      update: (store, result) => documentUpdate(
        store,
        result,
        (dataCache: DocumentQuery, { data: { changeValue: { success, value } } }: ChangeValueMutationResult) => {
          if (success) {
            const values: ValueType[] = dataCache.document.sheets!
              .find(sheet => sheet.id === props.sheet.id)
              .values.filter((v: ValueType) => v.id !== value.id)
            dataCache.document.sheets!.find(sheet => sheet.id === props.sheet.id)!.values = [...values, value] as any
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
    return { columns, rows, mergedCells, mergeCells, active, setActive, changeValue }
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
