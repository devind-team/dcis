<template lang="pug">
  div
    grid-sheet-toolbar(:update="update")
    table.grid__table
      grid-header(:columns="columns")
      grid-body(
        :rows="rows"
        :selection="selection"
        :start-selection="startCellSelection"
        :enter-selection="enterCellSelection"
        :end-selection="endCellSelection"
        :set-active="setActive"
      )
    pre {{ selectionCells }}
</template>

<script lang="ts">
import type { PropType, Ref } from '#app'
import { defineComponent, provide, toRef } from '#app'
import {
  AddRowDimensionMutation,
  DeleteRowDimensionMutation,
  SheetType
} from '~/types/graphql'
import { useGrid } from '~/composables/grid'
import GridHeader from '~/components/dcis/grid/GridHeader.vue'
import GridBody from '~/components/dcis/grid/GridBody.vue'
import GridSheetToolbar from '~/components/dcis/grid/GridSheetToolbar.vue'

export type AddRowDimensionMutationResult = { data: AddRowDimensionMutation }
export type DeleteRowDimensionMutationResult = { data: DeleteRowDimensionMutation }

type DocumentUpdateTransformType = (dc: any, result: any) => any
type DocumentUpdateType = (cache: any, result: any, transform: DocumentUpdateTransformType) => any

export default defineComponent({
  components: { GridSheetToolbar, GridBody, GridHeader },
  props: {
    documentId: { type: String, required: true },
    sheet: { type: Object as PropType<SheetType>, required: true },
    update: { type: Function as PropType<DocumentUpdateType>, required: true }
  },
  setup (props) {
    const sheet: Ref<SheetType> = toRef(props, 'sheet')
    const {
      columns,
      rows,
      mergeCells,
      mergedCells,
      active,
      selection,
      selectionCells,
      startCellSelection,
      enterCellSelection,
      endCellSelection,
      setActive
    } = useGrid(sheet)

    provide('active', active)
    provide('documentId', props.documentId)
    provide('documentUpdate', props.update)

    return {
      columns,
      rows,
      mergedCells,
      mergeCells,
      active,
      selection,
      selectionCells,
      startCellSelection,
      enterCellSelection,
      endCellSelection,
      setActive
    }
  }
})
</script>

<style lang="sass">
table.grid__table
  user-select: none

  margin-top: 3px
  border-collapse: collapse

  thead tr th, tbody tr td.row_index
    border: 1px solid silver
    text-align: center
    min-width: 25px
    cursor: pointer
    &:hover
      background: lightgray
  tbody tr td.grid__row-index
    font-weight: bold
    border: 1px solid silver
    text-align: center
  tbody tr td:not(.grid__row-index)
    border: 1px solid silver
    position: relative
    cursor: cell

    &.grid__cell-container-selected
      border: 1.2px blue solid !important

    .grid__cell-container-active
      top: 0
      left: 0
      position: absolute
      width: 100%
      height: 100%
      input
        width: 100%
        height: 100%
        &:focus
          outline: none

  tbody tr:hover
    background: rgba(0, 0, 0, .1)
</style>
