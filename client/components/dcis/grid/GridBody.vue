<template lang="pug">
  tbody
    tr(v-for="row in rows" :key="row.rowDimension.id" :style="row.style")
      td.grid__cell_row-index
      td(
        v-for="buildCell in row.cells"
        :key="buildCell.cell.id"
        :colspan="buildCell.colspan"
        :rowspan="buildCell.rowspan"
        :style="`${buildCell.style}`"
      )
        grid-cell(
          :build-cell="buildCell"
        )
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildRowType } from '~/types/grid'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true }
  }
})
</script>
