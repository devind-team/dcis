<template lang="pug">
.grid__body
  div.grid__container(ref="gridContainer" :style="{ height }")
    table.grid__table(:style="{ width: `${gridWidth}px` }" ref="grid")
      grid-header(
        :row-name-column-width="rowNameColumnWidth"
        :column-name-row-height="columnNameRowHeight"
        :resizing-column="resizingColumn"
        :get-column-width="getColumnWidth"
        :change-column-width="changeColumnWidth"
        :reset-column-width="resetColumnWidth"
        :get-column-fixed-info="getColumnFixedInfo"
        :border-fixed-column="borderFixedColumn"
        :border-fixed-row="borderFixedRow"
        :is-column-fixed-border="isColumnFixedBorder"
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
        :change-row-height="changeRowHeight"
        :reset-row-height="resetRowHeight"
        :get-row-fixed-info="getRowFixedInfo"
        :get-cell-fixed-info="getCellFixedInfo"
        :border-fixed-column="borderFixedColumn"
        :border-fixed-row="borderFixedRow"
        :is-row-fixed-border="isRowFixedBorder"
        :is-cell-fixed-border-right="isCellFixedBorderRight"
        :is-cell-fixed-border-bottom="isCellFixedBorderBottom"
        :selected-cells="selectedCells"
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
        :dblclick-cell="dblclickCell"
      )
    template(v-if="mode === GridMode.CHANGE")
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
    :message="String($t('dcis.grid.columnWidth'))"
    :element-resizing="resizingColumnWidth"
  )
  grid-element-resizing(
    :message="String($t('dcis.grid.rowHeight'))"
    :element-resizing="resizingRowHeight"
  )
</template>

<script lang="ts">
import { defineComponent, inject } from '#app'
import { GridModeInject, GridMode } from '~/types/grid'
import { useGrid } from '~/composables/grid'
import GridHeader from '~/components/dcis/grid/GridHeader.vue'
import GridBody from '~/components/dcis/grid/GridBody.vue'
import GridElementResizing from '~/components/dcis/grid/GridElementResizing.vue'
import GridSelectionView from '~/components/dcis/grid/GridSelectionView.vue'

export default defineComponent({
  components: {
    GridHeader,
    GridBody,
    GridElementResizing,
    GridSelectionView
  },
  props: {
    height: { type: String, required: true }
  },
  setup () {
    const mode = inject(GridModeInject)

    return {
      GridMode,
      mode,
      ...useGrid()
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

$resizing-background-light: white
$resizing-background-dark: #1E1E1E
$border: 1px solid silver
$border-selected: 1px solid blue
$border-fixed: 1.5px solid gray
$selected-light: #F3FAFF
$selected-dark: #DBF0FE
$readonly: map-get($grey, 'lighten-4')
$arrow-right-cursor: url("/cursors/arrow-right.svg") 8 8, pointer
$arrow-down-cursor: url("/cursors/arrow-down.svg") 8 8, pointer

div.grid__body
  line-height: 1.25

  .grid__element-resizing
    position: absolute
    z-index: 2
    font-size: 12px

  .grid__element-resizing_light
    background: $resizing-background-light !important

  .grid__element-resizing_dark
    background: $resizing-background-dark !important

  .grid__container
    position: relative
    overflow: auto

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
              border-color: transparent transparent $selected-light transparent

          &:hover

            & > div
              border-color: transparent transparent $selected-dark transparent

        th:not(:first-child)
          &.grid__header_selected

            & > div
              background: $selected-light !important

          &.grid__header_boundary-selected
            border-bottom: $border-selected

          &.grid__header_hover
            cursor: $arrow-down-cursor

            &:hover > div
              background: $selected-dark !important
              cursor: $arrow-down-cursor

          & > div
            display: flex
            justify-content: center
            align-items: center

          &.grid__header_fixed
            position: sticky
            z-index: 1

        th.grid__header_fixed-border-right
          border-right: $border-fixed

        th.grid__header_fixed-border-bottom
          border-bottom: $border-fixed

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
              background: $selected-light !important

          &.grid__cell_row-name-boundary-selected
            border-right: $border-selected

          &.grid__cell_row-name-hover
            cursor: $arrow-right-cursor

            &:hover > div
              background: $selected-dark !important
              cursor: $arrow-right-cursor

          & > div
            display: flex
            justify-content: center
            align-items: center

        td:not(.grid__cell_row-name)
          cursor: cell
          position: relative

          &.grid__cell_selected

            & > div
              background: $selected-light !important

          &.grid__cell_readonly

            & > div
              background: $readonly

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

        tr.grid__row_fixed
          position: sticky

        td.grid__cell_fixed
          position: sticky
          z-index: 1

        td.grid__cell_fixed-border-right
          border-right: $border-fixed

        td.grid__cell_fixed-border-bottom
          border-bottom: $border-fixed

    div.grid__selection-view
      position: absolute
      pointer-events: none
</style>
