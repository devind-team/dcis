<template lang="pug">
  div
    grid-sheet-toolbar(
      :sheet-id="sheet.id"
      :selection-cells="selectionCells"
      :selection-cells-options="selectionCellsOptions"
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
import type { PropType, Ref } from '#app'
import { defineComponent, provide, toRef } from '#app'
import {
  SheetType,
  ColumnDimensionType,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables
} from '~/types/graphql'
import { useOldGrid } from '~/composables/old-grid'
import changeColumnDimension from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import GridHeader from '~/components/dcis/grid/OldGridHeader.vue'
import GridBody from '~/components/dcis/grid/OldGridBody.vue'
import GridSheetToolbar from '~/components/dcis/grid/OldGridSheetToolbar.vue'
import GridColumnWidth from '~/components/dcis/grid/GridColumnWidth.vue'

export type DocumentUpdateTransformType = (dc: any, result: any) => any
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
        kind: columnDimension.kind
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
    } = useOldGrid(sheet, changeColumnWidth)

    provide<Ref<string>>('active', active)
    provide<string>('documentId', props.documentId)
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
