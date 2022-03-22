<template lang="pug">
  tbody
    tr(v-for="row in rows" :key="row.id" :style="row.style")
      td.grid__row-index
        grid-row-control(:row="row")
      td(
        v-for="cell in row.cells"
        :key="cell.id"
        :colspan="cell.colspan"
        :rowspan="cell.rowspan"
        :style="cell.style"
        @click="setActive(cell.position)"
      )
        grid-cell(
          @clear-active="setActive(null)"
          :cell="cell"
          :active="active === cell.position"
        )
</template>
<script lang="ts">
import type { PropType, Ref } from '#app'
import { defineComponent, inject } from '#app'
import { BuildRowType } from '~/types/grid-types'
import GridCell from '~/components/dcis/grid/GridCell.vue'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true },
    setActive: { type: Function as PropType<(position: string) => void>, required: true }
  },
  setup () {
    const active: Ref<string> = inject<Ref<string>>('active')
    return { active }
  }
})
</script>
