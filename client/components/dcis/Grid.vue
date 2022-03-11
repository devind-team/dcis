<template lang="pug">
  table.grid__table
    thead
      tr
        td.header-cell
        td(
          v-for="buildColumn in columns"
          :key="buildColumn.dimension.id"
          :style="buildColumn.style"
        ).header-cell {{ buildColumn.name }}
    tbody
      tr(
        v-for="buildRow in rows"
        :key="buildRow.dimension.id"
        :style="buildRow.style"
      )
        td.header-cell {{ buildRow.name }}
        td(
          v-for="buildCell in buildRow.cells"
          :key="buildCell.cell.id"
          :class="{ 'active-cell': isActive(buildCell) }"
          :colspan="buildCell.colspan"
          :rowspan="buildCell.rowspan"
          @click="activateCell(buildCell)"
          @dblclick="editCell(buildCell)"
        )
          template(v-if="isEditable(buildCell)")
            input.input(v-model="editableCell.newValue" v-focus)
          template(v-else) {{ buildCell.value.value }}
</template>

<script lang="ts">
import { computed, defineComponent } from '#app'
import type { ComputedRef, PropType } from '#app'
import { SheetType } from '~/types/graphql'

export default defineComponent({
  directives: {
    focus: {
      inserted (el) {
        el.focus()
      }
    }
  },
  props: {
    sheet: {
      type: Object as PropType<SheetType>,
      required: true
    }
  },
  setup (props) {
    const sheet: ComputedRef<SheetType> = computed<SheetType>(() => props.sheet)
    const { columns, rows, editableCell, isActive, isEditable, isCurrent, activateCell, editCell } = useGrid(sheet)
    return {
      columns, rows, editableCell, isActive, isEditable, isCurrent, activateCell, editCell
    }
  }
})
</script>

<style lang="sass">
.grid__table
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
