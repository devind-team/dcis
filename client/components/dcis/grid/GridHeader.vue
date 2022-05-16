<template lang="pug">
  thead
    tr
      th(:style="{ width: `${rowIndexColumnWidth}px` }" @click="selectAllCells")
        .grid__header-content
          .grid__select-all(:class="{ 'grid__select-all_selected': allCellsSelected }")
      th(
        v-for="buildColumn in columns"
        :key="buildColumn.columnDimension.id"
        :style="buildColumn.style"
        @mouseenter="mouseenterColumnIndex(buildColumn)"
        @mousemove="mousemoveColumnIndex(buildColumn, $event)"
        @mouseleave="mouseleaveColumnIndex"
        @mousedown="mousedownColumnIndex(buildColumn, $event)"
        @mouseup="mouseupColumnIndex"
      )
        grid-column-control(v-slot="{ on }" :build-column="buildColumn")
          div(
            :class="getHeaderContentClasses(buildColumn)"
            @contextmenu.prevent="on.click"
          ) {{ buildColumn.columnDimension.name }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildColumnType, BoundaryRowCell } from '~/types/grid'
import GridColumnControl from '~/components/dcis/grid/controls/GridColumnControl.vue'

export default defineComponent({
  components: { GridColumnControl },
  props: {
    rowIndexColumnWidth: { type: Number, required: true },
    columns: { type: Array as PropType<BuildColumnType[]>, required: true },
    selectedColumnPositions: { type: Array as PropType<number[]>, required: true },
    selectedBoundaryRowCells: { type: Array as PropType<BoundaryRowCell[]>, required: true },
    allCellsSelected: { type: Boolean, required: true },
    mouseenterColumnIndex: {
      type: Function as PropType<(buildColumn: BuildColumnType) => void>,
      required: true
    },
    mousemoveColumnIndex: {
      type: Function as PropType<(buildColumn: BuildColumnType, event: MouseEvent) => void>,
      required: true
    },
    mouseleaveColumnIndex: { type: Function as PropType<() => void>, required: true },
    mousedownColumnIndex: {
      type: Function as PropType<(buildColumn: BuildColumnType, event: MouseEvent) => void>,
      required: true
    },
    mouseupColumnIndex: { type: Function as PropType<() => void>, required: true },
    selectAllCells: { type: Function as PropType<() => void>, required: true }
  },
  setup (props) {
    const getHeaderContentClasses = (buildColumn: BuildColumnType): (string | Record<string, boolean>)[] => {
      return [
        'grid__header-content',
        { 'grid__header-content_selected': props.selectedColumnPositions.includes(buildColumn.columnDimension.index) },
        {
          'grid__header-content_neighbor-selected': !!props.selectedBoundaryRowCells.find(boundaryCell =>
            boundaryCell.buildColumns.find(boundaryRowColumn =>
              boundaryRowColumn.columnDimension.id === buildColumn.columnDimension.id))
        }
      ]
    }
    return {
      getHeaderContentClasses
    }
  }
})
</script>
