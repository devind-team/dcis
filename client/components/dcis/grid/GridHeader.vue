<template lang="pug">
thead
  tr(:style="{ height: `${columnNameRowHeight}px` }")
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
      :style="getHeaderStyle(column)"
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
import { GridMode, ResizingType, FixedInfoType } from '~/types/grid'
import { SheetType, ColumnDimensionType } from '~/types/graphql'
import GridColumnControl from '~/components/dcis/grid/controls/GridColumnControl.vue'

export default defineComponent({
  components: { GridColumnControl },
  props: {
    rowNameColumnWidth: { type: Number, required: true },
    columnNameRowHeight: { type: Number, required: true },
    resizingColumn: { type: Object as PropType<ResizingType<ColumnDimensionType>>, default: null },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true },
    getColumnFixedInfo: { type: Function as PropType<(column: ColumnDimensionType) => FixedInfoType>, required: true },
    selectedColumnPositions: { type: Array as PropType<number[]>, required: true },
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
        grid__header_hover: !props.resizingColumn,
        grid__header_fixed: props.getColumnFixedInfo(column).fixed
      }
    }
    const getHeaderStyle = (column: ColumnDimensionType): Record<string, string> => {
      return {
        width: `${props.getColumnWidth(column)}px`,
        left: `${props.getColumnFixedInfo(column).position}px`
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

    return { GridMode, mode, activeSheet, getHeaderClass, getHeaderStyle, posX, posY, currentCol, showMenu }
  }
})
</script>
