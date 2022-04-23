<template lang="pug">
  div
    grid-sheet-toolbar(
      :sheet-id="sheet.id"
      :selection-cells="selectionCells"
      :selection-cells-options="selectionCellsOptions"
      :update="update"
    )
    .grid__body
      div.grid__container(ref="gridContainer")
        table.grid__table(:style="{ width: `${gridWidth}px` }")
          grid-header(
            :row-index-column-width="rowIndexColumnWidth"
            :columns="columns"
            :selection-columns="selectionColumns"
            :all-selected="allSelected"
            :selected-boundary-row-cells="selectedBoundaryRowCells"
            :mouseenter-column-index="mouseenterColumnIndex"
            :mousemove-column-index="mousemoveColumnIndex"
            :mouseleave-column-index="mouseleaveColumnIndex"
            :mousedown-column-index="mousedownColumnIndex"
            :mouseup-column-index="mouseupColumnIndex"
            :select-all="selectAll"
          )
          grid-body(
            :rows="rows"
            :selection="selection"
            :selection-rows="selectionRows"
            :boundary-column-cells="boundaryColumnCells"
            :selected-boundary-column-cells="selectedBoundaryColumnCells"
            :mouseenter-row-index="mouseenterRowIndex"
            :mousedown-row-index="mousedownRowIndex"
            :start-selection="startCellSelection"
            :enter-selection="enterCellSelection"
            :end-selection="endCellSelection"
            :set-active="setActive"
          )
      grid-column-width(:visible="columnWidth.visible" :position="columnWidth.position" :width="columnWidth.width")
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import type { PropType } from '#app'
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
import GridColumnWidth from '~/components/dcis/grid/GridColumnWidth.vue'
import changeColumnDimension from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'

export type AddRowDimensionMutationResult = { data: AddRowDimensionMutation }
export type DeleteRowDimensionMutationResult = { data: DeleteRowDimensionMutation }

type DocumentUpdateTransformType = (dc: any, result: any) => any
type DocumentUpdateType = (cache: any, result: any, transform: DocumentUpdateTransformType) => any

export default defineComponent({
  components: { GridSheetToolbar, GridBody, GridHeader, GridColumnWidth },
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

    const sheet = toRef(props, 'sheet')
    const {
      rowIndexColumnWidth,
      gridWidth,
      columns,
      rows,
      mergeCells,
      mergedCells,
      active,
      selection,
      selectionCells,
      selectionColumns,
      selectionRows,
      allSelected,
      boundaryColumnCells,
      selectedBoundaryColumnCells,
      selectedBoundaryRowCells,
      selectionCellsOptions,
      startCellSelection,
      enterCellSelection,
      endCellSelection,
      setActive,
      gridContainer,
      columnWidth,
      mouseenterColumnIndex,
      mousemoveColumnIndex,
      mouseleaveColumnIndex,
      mousedownColumnIndex,
      mouseupColumnIndex,
      mouseenterRowIndex,
      mousedownRowIndex,
      selectAll
    } = useGrid(sheet, changeColumnWidth)

    provide('active', active)
    provide('documentId', props.documentId)
    provide('documentUpdate', props.update)

    return {
      rowIndexColumnWidth,
      gridWidth,
      columns,
      rows,
      mergedCells,
      mergeCells,
      active,
      selection,
      selectionCells,
      selectionColumns,
      selectionRows,
      allSelected,
      boundaryColumnCells,
      selectedBoundaryColumnCells,
      selectedBoundaryRowCells,
      selectionCellsOptions,
      startCellSelection,
      enterCellSelection,
      endCellSelection,
      setActive,
      gridContainer,
      columnWidth,
      mouseenterColumnIndex,
      mousemoveColumnIndex,
      mouseleaveColumnIndex,
      mousedownColumnIndex,
      mouseupColumnIndex,
      mouseenterRowIndex,
      mousedownRowIndex,
      selectAll
    }
  }
})
</script>

<style lang="sass">
@import '~vuetify/src/styles/styles.sass'

.grid__cursor_cell *
  cursor: cell !important
.grid__cursor_col-resize *
  cursor: col-resize !important

$border: 1px solid silver
$index-light: map-get($grey, 'lighten-3')
$index-dark: map-get($grey, 'lighten-2')

div.grid__body
  position: relative

  .grid__container
    position: relative
    height: calc(100vh - 230px)
    overflow: auto

    table.grid__table
      height: 1px
      user-select: none
      table-layout: fixed

      margin-top: 3px
      border-collapse: collapse

      td, th
        background-clip: padding-box

      thead
        position: sticky
        top: 0
        z-index: 2

        th
          height: 25px

          .grid__header-content
            position: relative
            left: 0.5px
            height: 100%
            overflow: hidden
            border-top: $border
            border-right: $border
            border-bottom: $border
            background: white

            &.grid__header-content_selected
              background: $index-light

        th:first-child
          position: sticky
          left: 0
          z-index: 2

          cursor: cell

          .grid__header-content
            left: 0
            width: calc(100% + 0.5px)
            border-left: $border

            .grid__select-all
              position: absolute
              right: 1px
              top: 1px

              width: 0
              height: 0
              border-style: solid
              border-width: 0 0 22px 22px
              border-color: transparent transparent transparent transparent

            .grid__select-all_selected
              border-color: transparent transparent $index-light transparent

          &:hover

            .grid__header-content

              .grid__select-all
                border-color: transparent transparent $index-dark transparent

        th:not(:first-child)
          cursor: url("/cursors/arrow-down.svg") 8 8, pointer

          .grid__header-content:hover
            background: $index-dark !important

      tbody
        tr:first-child

          td:not(.grid__cell_row-index)
            border-top: none !important

          .grid__cell-content_row-index
            top: 0 !important

        td:first-child
          cursor: url("/cursors/arrow-right.svg") 8 8, pointer

        td
          overflow: hidden

        td.grid__cell_row-index
          position: sticky
          height: 100%
          left: 0
          z-index: 1
          overflow: visible

          font-weight: bold
          text-align: center
          width: 30px

          .grid__cell-content_row-index
            position: relative
            top: 0.5px
            width: calc(100% + 0.5px)
            height: 100%
            border-right: $border
            border-bottom: $border
            border-left: $border
            background: white

            &.grid__cell-content_row-index-selected
              background: $index-light

            &:hover
              background: $index-dark !important

        td:not(.grid__cell_row-index)
          position: relative
          border: $border
          cursor: cell

          &.grid__cell_boundary
            border-left: none !important

          .grid__cell-content_active
            position: absolute
            width: 100%
            height: 100%
            top: 0
            left: 0

            input
              width: 100%
              height: 100%

              &:focus
                outline: none

@mixin grid__browser-specific($browser, $border-width, $first-row-index-height, $row-index-height)
  .browser-#{$browser}

    table.grid__table

      th

        .grid__header-content

          &.grid__header-content_neighbor-selected
            border-bottom: #{$border-width} solid blue !important

      tr:first-child

        .grid__cell-content_row-index
          height: #{$first-row-index-height} !important

      td.grid__cell_row-index
        height: #{$row-index-height} !important

        .grid__cell-content_row-index

          &.grid__cell-content_row-index-neighbor-selected
            border-right: #{$border-width} solid blue !important

      td:not(.grid__cell_row-index)

        &.grid__cell_selected
          border: #{$border-width} solid blue !important

@include grid__browser-specific('default', 1.2px, calc(100% + 1px), 1px)
@include grid__browser-specific('firefox', 2px, calc(100% + 0.5px), 100%)
</style>
