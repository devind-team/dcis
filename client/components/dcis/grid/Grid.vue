<template lang="pug">
.grid__body
  div.grid__container(ref="gridContainer" @scroll="gridContainerScroll")
    table.grid__table(:style="{ width: `${gridWidth}px` }" ref="grid")
      grid-header(
        :row-name-column-width="rowNameColumnWidth"
        :resizing-column="resizingColumn"
        :get-column-width="getColumnWidth"
        :selected-column-positions="selectedColumnsPositions"
        :boundary-selected-columns-positions="boundarySelectedColumnsPositions"
        :all-cells-selected="allCellsSelected"
        :mouseenter-column-name="mouseenterColumnName"
        :mousemove-column-name="mousemoveColumnName"
        :mouseleave-column-name="mouseleaveColumnName"
        :mousedown-column-name="mousedownColumnName"
        :mouseup-column-name="mouseupColumnName"
        :select-all-cells="selectAllCells"
      )
      grid-body(
        :resizing-row="resizingRow"
        :get-row-height="getRowHeight"
        :active-cell="activeCell"
        :set-active-cell="setActiveCell"
        :selected-rows-positions="selectedRowsPositions"
        :boundary-selected-rows-positions="boundarySelectedRowsPositions"
        :clear-selection="clearSelection"
        :mouseenter-row-name="mouseenterRowName"
        :mousemove-row-name="mousemoveRowName"
        :mouseleave-row-name="mouseleaveRowName"
        :mousedown-row-name="mousedownRowName"
        :mouseup-row-name="mouseupRowName"
        :mousedown-cell="mousedownCell"
        :mouseenter-cell="mouseenterCell"
        :mouseup-cell="mouseupCell"
      )
    grid-selection-view(
      v-if="columnsSelectionView"
      :key="columnsSelectionView.id"
      :selection-view="columnsSelectionView"
    )
    grid-selection-view(
      v-if="rowsSelectionView"
      :key="rowsSelectionView.id"
      :selection-view="rowsSelectionView"
    )
    template(v-if="cellsSelectionView")
      grid-selection-view(
        v-for="view in cellsSelectionView"
        :selection-view="view"
        :key="view.id"
      )
  grid-element-resizing(
    :message="String(t('dcis.grid.columnWidth'))"
    :element-resizing="resizingColumnWidth"
  )
  grid-element-resizing(
    :message="String(t('dcis.grid.rowHeight'))"
    :element-resizing="resizingRowHeight"
  )
</template>

<script lang="ts">
import { defineComponent, Ref, PropType, toRef, provide } from '#app'
import { GridMode, UpdateSheetType } from '~/types/grid'
import { DocumentType, SheetType, RowDimensionType, DocumentsSheetQuery, DocumentSheetQuery } from '~/types/graphql'
import {
  UpdateType,
  useChangeColumnDimensionWidthMutation,
  useChangeRowDimensionHeightMutation,
  useChangeChildRowDimensionHeightMutation,
  useGrid,
  useI18n
} from '~/composables'
import { useAuthStore } from '~/stores'
import GridHeader from '~/components/dcis/grid/GridHeader.vue'
import GridBody from '~/components/dcis/grid/GridBody.vue'
import GridSelectionView from '~/components/dcis/grid/GridSelectionView.vue'
import GridElementResizing from '~/components/dcis/grid/GridElementResizing.vue'

export default defineComponent({
  components: {
    GridHeader,
    GridBody,
    GridSelectionView,
    GridElementResizing
  },
  props: {
    mode: { type: Number, required: true },
    activeSheet: { type: Object as PropType<SheetType>, required: true },
    updateActiveSheet: { type: Function as PropType<UpdateSheetType>, required: true },
    activeDocument: { type: Object as PropType<DocumentType>, default: null }
  },
  setup (props) {
    const { t } = useI18n()

    const userStore = useAuthStore()

    const activeSheet = toRef(props, 'activeSheet')
    const updateActiveSheet = toRef(props, 'updateActiveSheet')
    const activeDocument = toRef(props, 'activeDocument')

    provide('mode', props.mode)
    provide('activeSheet', activeSheet)
    provide('updateActiveSheet', updateActiveSheet)
    provide('activeDocument', activeDocument)

    const canChangeRowHeight = (rowDimension: RowDimensionType) => {
      if (props.mode === GridMode.CHANGE) {
        return true
      }
      if (!activeDocument.value.lastStatus.status.edit) {
        return false
      }
      return rowDimension.parent !== null && (activeSheet.value.canChange || userStore.user.id === rowDimension.userId)
    }

    const changeColumnWidth = props.mode === GridMode.CHANGE
      ? useChangeColumnDimensionWidthMutation(updateActiveSheet as Ref<UpdateType<DocumentsSheetQuery>>)
      : null
    const changeRowHeight = props.mode === GridMode.CHANGE
      ? useChangeRowDimensionHeightMutation(updateActiveSheet as Ref<UpdateType<DocumentsSheetQuery>>)
      : useChangeChildRowDimensionHeightMutation(updateActiveSheet as Ref<UpdateType<DocumentSheetQuery>>)

    const {
      gridContainer,
      grid,
      resizingColumn,
      resizingColumnWidth,
      getColumnWidth,
      resizingRow,
      resizingRowHeight,
      getRowHeight,
      gridWidth,
      rowNameColumnWidth,
      activeCell,
      setActiveCell,
      cellsSelectionView,
      rowsSelectionView,
      columnsSelectionView,
      boundarySelectedColumnsPositions,
      boundarySelectedRowsPositions,
      allCellsSelected,
      selectedColumnsPositions,
      selectedRowsPositions,
      selectedCellsOptions,
      clearSelection,
      selectAllCells,
      gridContainerScroll,
      mousedownCell,
      mouseenterCell,
      mouseupCell,
      mouseenterColumnName,
      mousemoveColumnName,
      mouseleaveColumnName,
      mousedownColumnName,
      mouseupColumnName,
      mouseenterRowName,
      mousemoveRowName,
      mouseleaveRowName,
      mousedownRowName,
      mouseupRowName
    } = useGrid(props.mode, activeSheet, canChangeRowHeight, changeColumnWidth, changeRowHeight)

    return {
      t,
      gridContainer,
      grid,
      resizingColumn,
      resizingColumnWidth,
      getColumnWidth,
      resizingRow,
      resizingRowHeight,
      getRowHeight,
      gridWidth,
      rowNameColumnWidth,
      activeCell,
      setActiveCell,
      cellsSelectionView,
      rowsSelectionView,
      columnsSelectionView,
      boundarySelectedColumnsPositions,
      boundarySelectedRowsPositions,
      allCellsSelected,
      selectedColumnsPositions,
      selectedRowsPositions,
      selectedCellsOptions,
      clearSelection,
      selectAllCells,
      gridContainerScroll,
      mousedownCell,
      mouseenterCell,
      mouseupCell,
      mouseenterColumnName,
      mousemoveColumnName,
      mouseleaveColumnName,
      mousedownColumnName,
      mouseupColumnName,
      mouseenterRowName,
      mousemoveRowName,
      mouseleaveRowName,
      mousedownRowName,
      mouseupRowName
    }
  }
})
</script>

<style lang="sass">
@import '~vuetify/src/styles/styles'

.grid__cursor_cell *
  cursor: cell !important
.grid__cursor_col-resize *
  cursor: col-resize !important
.grid__cursor_row-resize *
  cursor: row-resize !important

$border: 1px solid silver
$border-selected: 1px solid blue
$name-light: map-get($grey, 'lighten-3')
$name-dark: map-get($grey, 'lighten-2')
$arrow-right-cursor: url("/cursors/arrow-right.svg") 8 8, pointer
$arrow-down-cursor: url("/cursors/arrow-down.svg") 8 8, pointer

div.grid__body
  .grid__element-resizing
    position: absolute
    z-index: 2
    font-size: 12px
    background: white !important

  .grid__container
    position: relative
    overflow: auto
    height: calc(100vh - 337px)

    table.grid__table
      height: 1px
      user-select: none
      table-layout: fixed
      border-spacing: 0

      td, th
        overflow: hidden
        color: rgba(0, 0, 0, 0.87)
        background: white
        background-clip: padding-box
        border-right: $border
        border-bottom: $border

        & > div
          background: white

      thead
        position: sticky
        top: 0
        z-index: 2

        th
          height: 25px
          border-top: $border
          font-size: 16px

          & > div:first-child
            height: 100%

        th:first-child
          position: sticky
          left: 0
          cursor: cell
          border-left: $border

          & > div
            position: absolute
            right: 1px
            top: 1px
            width: 0
            height: 0
            border-style: solid
            border-width: 0 0 22px 22px
            border-color: transparent transparent transparent transparent

          &.grid__header_all_selected

            & > div
              border-color: transparent transparent $name-light transparent

          &:hover

            & > div
              border-color: transparent transparent $name-dark transparent

        th:not(:first-child)
          &.grid__header_selected

            & > div
              background: $name-light !important

          &.grid__header_boundary-selected
            border-bottom: $border-selected

          &.grid__header_hover
            cursor: $arrow-down-cursor

            &:hover > div
              background: $name-dark !important
              cursor: $arrow-down-cursor

          & > div
            display: flex
            justify-content: center
            align-items: center

      tbody
        td.grid__cell_row-name
          position: sticky
          height: 100%
          left: 0
          z-index: 1
          border-left: $border
          font-size: 16px
          font-weight: bold

          &.grid__cell_row-name-selected

            & > div
              background: $name-light !important

          &.grid__cell_row-name_boundary-selected
            border-right: $border-selected

          &.grid__cell_row-name-hover
            cursor: $arrow-right-cursor

            &:hover > div
              background: $name-dark !important
              cursor: $arrow-right-cursor

          & > div
            display: flex
            justify-content: center
            align-items: center

        td:not(.grid__cell_row-name)
          cursor: cell
          position: relative

          .grid__cell-content
            display: flex

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

    div.grid__selection-view
      position: absolute
      pointer-events: none
</style>
