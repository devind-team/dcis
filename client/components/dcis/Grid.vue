<template lang="pug">
  div
    grid-sheet-toolbar
    .grid__body
      div.grid__container(ref="gridContainer")
        table.grid__table(:style="{ width: `${gridWidth}px` }")
          grid-header(
            :row-name-column-width="rowNameColumnWidth"
            :columns="columns"
            :resizing-column="resizingColumn"
            :get-column-width="getColumnWidth"
            :selected-column-positions="selectedColumnsPositions"
            :selected-boundary-row-cells="selectedBoundaryRowCells"
            :all-cells-selected="allCellsSelected"
            :mouseenter-column-name="mouseenterColumnName"
            :mousemove-column-name="mousemoveColumnName"
            :mouseleave-column-name="mouseleaveColumnName"
            :mousedown-column-name="mousedownColumnName"
            :mouseup-column-name="mouseupColumnName"
            :select-all-cells="selectAllCells"
          )
          grid-body(
            :rows="rows"
            :resizing-row="resizingRow"
            :get-row-height="getRowHeight"
            :active-cell="activeCell"
            :set-active-cell="setActiveCell"
            :selected-cells-positions="selectedCellsPositions"
            :selected-rows-positions="selectedRowsPositions"
            :boundary-column-cells="boundaryColumnCells"
            :selected-boundary-column-cells="selectedBoundaryColumnCells"
            :mouseenter-row-name="mouseenterRowName"
            :mousemove-row-name="mousemoveRowName"
            :mouseleave-row-name="mouseleaveRowName"
            :mousedown-row-name="mousedownRowName"
            :mouseup-row-name="mouseupRowName"
            :mousedown-cell="mousedownCell"
            :mouseenter-cell="mouseenterCell"
            :mouseup-cell="mouseupCell"
          )
      grid-element-resizing(
        :message="String(t('dcis.grid.columnWidth'))"
        :visible="resizingColumnWidth.visible"
        :position="resizingColumnWidth.position"
        :size="resizingColumnWidth.size"
      )
      grid-element-resizing(
        :message="String(t('dcis.grid.rowHeight'))"
        :visible="resizingRowHeight.visible"
        :position="resizingRowHeight.position"
        :size="resizingRowHeight.size"
      )
</template>

<script lang="ts">
import { Ref } from '#app'
import { SheetType } from '~/types/graphql'
import GridSheetToolbar from '~/components/dcis/grid/GridSheetToolbar.vue'
import GridHeader from '~/components/dcis/grid/GridHeader.vue'
import GridBody from '~/components/dcis/grid/GridBody.vue'
import GridElementResizing from '~/components/dcis/grid/GridElementResizing.vue'

export default defineComponent({
  components: { GridSheetToolbar, GridHeader, GridBody, GridElementResizing },
  setup () {
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const { t } = useI18n()
    const {
      gridContainer,
      resizingColumn,
      resizingColumnWidth,
      getColumnWidth,
      resizingRow,
      resizingRowHeight,
      getRowHeight,
      gridWidth,
      rows,
      columns,
      rowNameColumnWidth,
      activeCell,
      setActiveCell,
      allCellsSelected,
      selectedCellsPositions,
      selectedColumnsPositions,
      selectedRowsPositions,
      selectedCellsOptions,
      mousedownCell,
      mouseenterCell,
      mouseupCell,
      boundaryColumnCells,
      selectedBoundaryColumnCells,
      boundaryRowCells,
      selectedBoundaryRowCells,
      mouseenterColumnName,
      mousemoveColumnName,
      mouseleaveColumnName,
      mousedownColumnName,
      mouseupColumnName,
      mouseenterRowName,
      mousemoveRowName,
      mouseleaveRowName,
      mousedownRowName,
      mouseupRowName,
      selectAllCells
    } = useGrid(activeSheet, () => {}, () => {})

    provide('rows', rows)
    provide('columns', columns)

    return {
      t,
      gridContainer,
      resizingColumn,
      resizingColumnWidth,
      getColumnWidth,
      resizingRow,
      resizingRowHeight,
      getRowHeight,
      gridWidth,
      rows,
      columns,
      rowNameColumnWidth,
      activeCell,
      setActiveCell,
      allCellsSelected,
      selectedCellsPositions,
      selectedColumnsPositions,
      selectedRowsPositions,
      selectedCellsOptions,
      mousedownCell,
      mouseenterCell,
      mouseupCell,
      boundaryColumnCells,
      selectedBoundaryColumnCells,
      boundaryRowCells,
      selectedBoundaryRowCells,
      mouseenterColumnName,
      mousemoveColumnName,
      mouseleaveColumnName,
      mousedownColumnName,
      mouseupColumnName,
      mouseenterRowName,
      mousemoveRowName,
      mouseleaveRowName,
      mousedownRowName,
      mouseupRowName,
      selectAllCells
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
.grid__cursor_row-resize *
  cursor: row-resize !important

$border: 1px solid silver
$name-light: map-get($grey, 'lighten-3')
$name-dark: map-get($grey, 'lighten-2')

div.grid__body
  position: relative

  .grid__element-resizing
    position: absolute
    z-index: 2
    font-size: 12px
    background: white !important

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
              background: $name-light

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
              border-color: transparent transparent $name-light transparent

          &:hover

            .grid__header-content

              .grid__select-all
                border-color: transparent transparent $name-dark transparent

        th:not(:first-child)

          .grid__header-content
            display: flex
            justify-content: center
            align-items: center

        th:not(:first-child).grid__header_hover
          cursor: url("/cursors/arrow-down.svg") 8 8, pointer

          .grid__header-content:hover
            background: $name-dark !important

      tbody
        tr:first-child

          td:not(.grid__cell_row-name)
            border-top: none !important

        td
          overflow: hidden

        td.grid__cell_row-name
          position: sticky
          height: 100%
          left: 0
          z-index: 1
          overflow: visible

          font-weight: bold

          .grid__cell-content_row-name
            display: flex
            justify-content: center
            align-items: center
            position: relative
            overflow: hidden
            top: 0.5px
            width: calc(100% + 0.5px)
            border-right: $border
            border-bottom: $border
            border-left: $border
            background: white

            &.grid__cell-content_row-name-selected
              background: $name-light

        td.grid__cell_row-name-hover
          cursor: url("/cursors/arrow-right.svg") 8 8, pointer

          .grid__cell-content_row-name:hover
            background: $name-dark !important

        td:not(.grid__cell_row-name)
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

@mixin grid__browser-specific($browser, $border-width)
  .browser-#{$browser}

    table.grid__table

      th

        .grid__header-content

          &.grid__header-content_neighbor-selected
            border-bottom: #{$border-width} solid blue !important

      td.grid__cell_row-name

        .grid__cell-content_row-name

          &.grid__cell-content_row-name-neighbor-selected
            border-right: #{$border-width} solid blue !important

      td:not(.grid__cell_row-name)

        &.grid__cell_selected
          border: #{$border-width} solid blue !important

@include grid__browser-specific('default', 1.2px)
@include grid__browser-specific('firefox', 2px)
</style>
