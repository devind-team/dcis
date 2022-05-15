<template lang="pug">
  tbody
    tr(v-for="buildRow in rows" :key="buildRow.rowDimension.id" :style="buildRow.style")
      td.grid__cell_row-index
        grid-row-control(:build-row="buildRow")
      td(
        v-for="buildCell in buildRow.buildCells"
        :key="buildCell.cell.id"
        :colspan="buildCell.cell.colspan"
        :rowspan="buildCell.cell.rowspan"
        :style="`${buildCell.style}`"
      )
        grid-cell(
          :build-cell="buildCell"
        )
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildRowType } from '~/types/grid'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'
import GridCell from '~/components/dcis/grid/GridCell.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true }
  }
})
</script>
