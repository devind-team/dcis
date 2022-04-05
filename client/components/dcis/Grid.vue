<template lang="pug">
  div
    grid-sheet-toolbar(
      :sheet-id="sheet.id"
      :selection-cells="selectionCells"
      :selection-cells-options="selectionCellsOptions"
      :update="update"
    )
    div.grid__container
      table.grid__table
        grid-header(
          :columns="columns"
          :move-column-header="moveColumnHeader"
          :leave-column-header="leaveColumnHeader"
          :start-column-resizing="startColumnResizing"
          :end-column-resizing="endColumnResizing"
          :style="{ cursor }"
        )
        grid-body(
          :rows="rows"
          :selection="selection"
          :start-selection="startCellSelection"
          :enter-selection="enterCellSelection"
          :end-selection="endCellSelection"
          :set-active="setActive"
        )
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { PropType, Ref } from '#app'
import { defineComponent, provide, toRef } from '#app'
import {
  SheetType,
  ColumnDimensionType,
  AddRowDimensionMutation,
  DeleteRowDimensionMutation,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables
} from '~/types/graphql'
import { useGrid } from '~/composables/grid'
import GridHeader from '~/components/dcis/grid/GridHeader.vue'
import GridBody from '~/components/dcis/grid/GridBody.vue'
import GridSheetToolbar from '~/components/dcis/grid/GridSheetToolbar.vue'
import changeColumnDimension from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'

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
    const changeColumnWidth = (columnDimension: ColumnDimensionType, width: number) => {
      const { mutate } = useMutation<ChangeColumnDimensionMutation, ChangeColumnDimensionMutationVariables>(
        changeColumnDimension
      )
      mutate({
        id: columnDimension.id,
        width,
        fixed: columnDimension.fixed,
        hidden: columnDimension.hidden,
        autoSize: columnDimension.autoSize
      }, {
        optimisticResponse: {
          changeColumnDimension: {
            __typename: 'ChangeColumnDimensionPayload',
            success: true,
            errors: [],
            columnDimension: {
              __typename: 'ColumnDimensionType',
              ...columnDimension,
              width
            }
          }
        }
      })
    }

    const sheet: Ref<SheetType> = toRef(props, 'sheet')
    const {
      columns,
      rows,
      mergeCells,
      mergedCells,
      active,
      selection,
      selectionCells,
      selectionCellsOptions,
      startCellSelection,
      enterCellSelection,
      endCellSelection,
      setActive,
      cursor,
      moveColumnHeader,
      leaveColumnHeader,
      startColumnResizing,
      endColumnResizing
    } = useGrid(sheet, changeColumnWidth)

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
      selectionCellsOptions,
      startCellSelection,
      enterCellSelection,
      endCellSelection,
      setActive,
      cursor,
      moveColumnHeader,
      leaveColumnHeader,
      startColumnResizing,
      endColumnResizing
    }
  }
})
</script>

<style lang="sass">
div.grid__container
  overflow: auto
  height: calc(100vh - 230px)
  position: relative

  table.grid__table
    user-select: none
    table-layout: fixed

    margin-top: 3px
    border-collapse: collapse

    thead
      position: sticky
      top: 0
      z-index: 2

      tr th
        background: white
        box-shadow: 1px 1px silver, -1px -1px silver

    tbody tr:hover
      background: rgba(0, 0, 0, 0.1) !important

    tbody tr td.grid__row-index
      font-weight: bold
      border: 1px solid silver
      text-align: center
      width: 30px

      position: sticky
      left: -1px
      z-index: 1

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
</style>
