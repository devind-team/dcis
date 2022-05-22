<template lang="pug">
  thead
    tr
      th(
        :class="{ 'grid__header_all_selected': allCellsSelected }"
        :style="{ width: `${rowNameColumnWidth}px` }"
        @click="selectAllCells"
      )
        div
      th(
        v-for="column in activeSheet.columns"
        :key="column.id"
        :class="getHeaderClass(column)"
        :style="{ 'width': `${getColumnWidth(column)}px` }"
        @mouseenter="mouseenterColumnName(column)"
        @mousemove="mousemoveColumnName(column, $event)"
        @mouseleave="mouseleaveColumnName"
        @mousedown="mousedownColumnName(column, $event)"
        @mouseup="mouseupColumnName"
      )
        grid-column-control(v-slot="{ on }" :column="column" :get-column-width="getColumnWidth")
          div(@contextmenu.prevent="on.click") {{ column.name }}
</template>

<script lang="ts">
import { PropType, Ref } from '#app'
import { SheetType, ColumnDimensionType } from '~/types/graphql'
import { ResizingType } from '~/types/grid'
import GridColumnControl from '~/components/dcis/grid/controls/GridColumnControl.vue'

export default defineComponent({
  components: { GridColumnControl },
  props: {
    rowNameColumnWidth: { type: Number, required: true },
    resizingColumn: { type: Object as PropType<ResizingType<ColumnDimensionType>>, default: null },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true },
    selectedColumnPositions: { type: Array as PropType<number[]>, required: true },
    boundarySelectedColumnsPositions: { type: Array as PropType<number[]>, required: true },
    allCellsSelected: { type: Boolean, required: true },
    mouseenterColumnName: {
      type: Function as PropType<(column: ColumnDimensionType) => void>,
      required: true
    },
    mousemoveColumnName: {
      type: Function as PropType<(column: ColumnDimensionType, event: MouseEvent) => void>,
      required: true
    },
    mouseleaveColumnName: { type: Function as PropType<() => void>, required: true },
    mousedownColumnName: {
      type: Function as PropType<(column: ColumnDimensionType, event: MouseEvent) => void>,
      required: true
    },
    mouseupColumnName: { type: Function as PropType<() => void>, required: true },
    selectAllCells: { type: Function as PropType<() => void>, required: true }
  },
  setup (props) {
    const activeSheet = inject<Ref<SheetType>>('activeSheet')

    const getHeaderClass = (column: ColumnDimensionType): Record<string, boolean> => {
      return {
        grid__header_selected: props.selectedColumnPositions.includes(column.index),
        'grid__header_boundary-selected': props.boundarySelectedColumnsPositions.includes(column.index),
        grid__header_hover: !props.resizingColumn
      }
    }

    return { activeSheet, getHeaderClass }
  }
})
</script>
