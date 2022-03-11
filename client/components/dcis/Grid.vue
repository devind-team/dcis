<template lang="pug">
  table.grid__table
    thead
      tr
        td.header
        td(
          v-for="buildColumn in columns"
          :key="buildColumn.dimension.id"
          :style="buildColumn.style"
        ).header {{ buildColumn.name }}
    tbody
      tr(
        v-for="buildRow in rows"
        :key="buildRow.dimension.id"
        :style="buildRow.style"
      )
        td.header {{ buildRow.name }}
        td(
          v-for="buildCell in buildRow.cells"
          :key="buildCell.cell.id"
          :colspan="buildCell.colspan"
          :rowspan="buildCell.rowspan"
        ) {{ buildCell.value.value }}
</template>

<script lang="ts">
import { computed, defineComponent } from '#app'
import type { ComputedRef, PropType } from '#app'
import { SheetType } from '~/types/graphql'

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
  user-select: none
  .header
    text-align: center
    background: lightgrey
  thead
    td
      height: 35px
      border: 1px solid grey
  tbody
    .header
      width: 30px
    td
      border: 1px solid grey
</style>
