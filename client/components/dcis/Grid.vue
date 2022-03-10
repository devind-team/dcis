<template lang="pug">
  table.grid__table
    thead
      tr
        td
        td(
          v-for="column in columns"
          :key="`column${column.name}`"
          :style="column.style"
        ) {{ column.name }}
    tbody
      tr(
        v-for="row in rows"
        :key="`row${row.rowIndex}`"
        :style="row.style"
      )
        td {{ row.rowIndex }}
        td(v-for="cell in row.buildCells" :key="`cell${cell.position}`") {{ cell.originCell.value }}
</template>

<script lang="ts">
import { computed, defineComponent } from '#app'
import type { ComputedRef, PropType } from '#app'
import { SheetType } from '~/types/dcis'
import { useGrid } from '~/composables/grid'

export default defineComponent({
  props: {
    sheet: {
      type: Object as PropType<SheetType>,
      required: true
    }
  },
  setup (props) {
    const sheet: ComputedRef<SheetType> = computed<SheetType>(() => props.sheet)
    const { columns, rows } = useGrid(sheet)
    return {
      columns, rows
    }
  }
})
</script>

<style lang="sass">
.grid__table
  border-collapse: collapse
  thead
    td
      border: 1px solid grey
  tbody
    td
      border: 1px solid grey
</style>
