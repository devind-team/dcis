<template lang="pug">
html(lang="ru")
  head
    meta(charset="utf-8")
    meta(name="viewport" content="width=device-width, initial-scale=1")
  body
    table(style="border-spacing: 0; border-collapse: collapse")
      tbody
        tr(v-for="(row, rowIndex) in selectedCells" :style="withStyles ? getRowStyle(rowIndex) : null")
          td(
            v-for="cell in row"
            :colspan="cell.colspan"
            :rowspan="cell.rowspan"
            :style="withStyles ? getCellStyle(cell) : null"
          ) {{ cell.value }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { CellType, ColumnDimensionType, RowDimensionType, SheetType } from '~/types/graphql'
import {
  parsePosition,
  getCellWidthStyle,
  getCellHeightStyle,
  getCellTextFormattingStyle,
  getCellBorderStyle,
  getCellBackgroundStyle,
  getCellExcelStyle,
  getCellTextAlignmentStyle
} from '~/services/grid'

export default defineComponent({
  props: {
    selectedCells: { type: Array as PropType<CellType[][]>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
    activeSheet: { type: Object as PropType<SheetType>, required: true },
    withStyles: { type: Boolean, required: true }
  },
  setup (props) {
    const getRowStyle = (rowIndex: number) => {
      const rowStartIndex = parsePosition(props.selectedCells[0][0].globalPosition).row
      return {
        height: `${props.getRowHeight(props.activeSheet.rows[rowStartIndex + rowIndex - 1])}px`
      }
    }
    const getCellStyle = (cell: CellType) => {
      const style = {
        ...getCellWidthStyle(cell, props.getColumnWidth, props.activeSheet),
        ...getCellHeightStyle(cell, props.getRowHeight, props.activeSheet),
        ...getCellTextFormattingStyle(cell),
        ...getCellTextAlignmentStyle(cell),
        ...getCellBorderStyle(cell),
        ...getCellBackgroundStyle(cell, props.activeSheet),
        ...getCellExcelStyle(cell)
      }
      for (const position of ['top', 'right', 'bottom', 'left']) {
        if (!style[`border-${position}`]) {
          style[`border-${position}`] = '1px solid silver'
        }
      }
      return style
    }

    return { getRowStyle, getCellStyle }
  }
})
</script>
