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
          input(v-if="active === cell.position" v-focus :value="cell.value" style="width: 100%;")
          template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { defineComponent } from '#app'
import type { PropType } from '#app'
import { SheetType } from '~/types/graphql'
import { useGrid } from '~/composables/grid'

export default defineComponent({
  directives: {
    focus: {
      inserted (el) {
        el.focus()
      }
    }
  },
  props: {
    sheet: { type: Object as PropType<SheetType>, required: true }
  },
  setup (props) {
    const {
      columns,
      rows,
      mergeCells,
      mergedCells,
      active,
      setActive
    } = useGrid(props.sheet)
    return { columns, rows, mergedCells, mergeCells, active, setActive }
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
