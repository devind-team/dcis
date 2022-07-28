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
      div(@contextmenu="(e) => showMenu(e, column)") {{ column.name }}
  grid-column-control(
    v-if="!!currentCol && mode === GridMode.CHANGE"
    :column="currentCol"
    :get-column-width="getColumnWidth"
    :pos-x="posX"
    :pos-y="posY"
    @close="currentCol = null"
  )
</template>

<script lang="ts">
import { nextTick, PropType, Ref } from '#app'
import { GridMode, ResizingType } from '~/types/grid'
import { SheetType, ColumnDimensionType } from '~/types/graphql'
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
    const mode = inject<GridMode>('mode')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')

    const getHeaderClass = (column: ColumnDimensionType): Record<string, boolean> => {
      return {
        grid__header_selected: props.selectedColumnPositions.includes(column.index),
        'grid__header_boundary-selected': props.boundarySelectedColumnsPositions.includes(column.index),
        grid__header_hover: !props.resizingColumn
      }
    }

    const currentCol = ref<ColumnDimensionType>(null)
    const posX = ref(0)
    const posY = ref(0)
    const showMenu = (e: MouseEvent, col: ColumnDimensionType) => {
      e.preventDefault()
      currentCol.value = null
      posY.value = e.clientY
      posX.value = e.clientX
      nextTick(() => {
        currentCol.value = col
      })
    }

    return { GridMode, mode, activeSheet, posX, posY, currentCol, showMenu, getHeaderClass }
  }
})
</script>
