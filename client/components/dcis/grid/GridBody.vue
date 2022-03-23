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
        :class="getCellClasses(cell)"
        :style="`${cell.style};${cell.border}`"
        @mousedown="startSelection($event, cell.position)"
        @mouseenter="enterSelection($event, cell.position)"
        @mouseup="endSelection($event, cell.position)"
      )
        grid-cell(
          @clear-active="setActive(null)"
          :cell="cell"
          :active="active === cell.position"
          :selection="selection && selection.includes(cell.position)"
        )
</template>
<script lang="ts">
import type { PropType, Ref } from '#app'
import { defineComponent, inject } from '#app'
import { BuildCellType, BuildRowType, RangeType } from '~/types/grid-types'
import GridCell from '~/components/dcis/grid/GridCell.vue'
import GridRowControl from '~/components/dcis/grid/controls/GridRowControl.vue'

export default defineComponent({
  components: { GridRowControl, GridCell },
  props: {
    rows: { type: Array as PropType<BuildRowType[]>, required: true },
    selection: { type: Array as PropType<RangeType[]>, default: () => ([]) },
    setActive: { type: Function as PropType<(position: string) => void>, required: true },
    startSelection: { type: Function as PropType<(e: MouseEvent, position: string) => void>, required: true },
    enterSelection: { type: Function as PropType<(e: MouseEvent, position: string) => void>, required: true },
    endSelection: { type: Function as PropType<(e: MouseEvent, position: string) => void>, required: true }
  },
  setup (props) {
    const active: Ref<string> = inject<Ref<string>>('active')

    const getCellClasses = (cell: BuildCellType): Record<string, boolean> => ({
      'grid__cell-container-selected': props.selection.includes(cell.position)
    })

    return { active, getCellClasses }
  }
})
</script>
