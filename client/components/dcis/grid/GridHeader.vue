<template lang="pug">
thead
  tr(:style="{ height: `${columnNameRowHeight}px` }")
    th(
      :class="firstHeaderClass"
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
import { ref, nextTick, PropType, computed } from '#app'
import { GridModeInject, ActiveSheetInject, GridMode, FixedInfoType, ResizingType } from '~/types/grid'
import { ColumnDimensionType, RowDimensionType } from '~/types/graphql'
import GridColumnControl from '~/components/dcis/grid/controls/GridColumnControl.vue'

export default defineComponent({
  components: { GridColumnControl },
  props: {
    rowNameColumnWidth: { type: Number, required: true },
    columnNameRowHeight: { type: Number, required: true },
    resizingColumn: { type: Object as PropType<ResizingType<ColumnDimensionType>>, default: null },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true },
    getColumnFixedInfo: { type: Function as PropType<(column: ColumnDimensionType) => FixedInfoType>, required: true },
    borderFixedColumn: { type: Object as PropType<ColumnDimensionType>, default: null },
    borderFixedRow: { type: Object as PropType<RowDimensionType>, default: null },
    isColumnFixedBorder: { type: Function as PropType<(column: ColumnDimensionType) => boolean>, required: true },
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
    const mode = inject(GridModeInject)
    const activeSheet = inject(ActiveSheetInject)

    const isFixedSelection = computed<boolean>(() =>
      mode.value === GridMode.READ || mode.value === GridMode.REPORT || mode.value === GridMode.WRITE
    )

    const firstHeaderClass = computed<Record<string, boolean>>(() => ({
      grid__header_all_selected: props.allCellsSelected,
      'grid__header_fixed-border-right': isFixedSelection.value && props.borderFixedColumn === null,
      'grid__header_fixed-border-bottom': isFixedSelection.value && props.borderFixedRow === null
    }))

    const getHeaderClass = (column: ColumnDimensionType): Record<string, boolean> => {
      return {
        grid__header_selected: props.selectedColumnPositions.includes(column.index),
        'grid__header_boundary-selected': mode.value === GridMode.CHANGE &&
          props.boundarySelectedColumnsPositions.includes(column.index),
        grid__header_hover: mode.value === GridMode.CHANGE && !props.resizingColumn,
        grid__header_fixed: isFixedSelection.value && props.getColumnFixedInfo(column).fixed,
        'grid__header_fixed-border-right': isFixedSelection.value && props.isColumnFixedBorder(column),
        'grid__header_fixed-border-bottom': isFixedSelection.value && props.borderFixedRow === null
      }
    }
    const getHeaderStyle = (column: ColumnDimensionType): Record<string, string> => {
      const style: Record<string, string> = {
        width: `${props.getColumnWidth(column)}px`
      }
      const fixedInfo = props.getColumnFixedInfo(column)
      if (fixedInfo.fixed) {
        style.left = `${fixedInfo.position}px`
      }
      return style
    }

    const currentCol = ref<ColumnDimensionType | null>(null)
    const posX = ref<number>(0)
    const posY = ref<number>(0)
    const showMenu = (e: MouseEvent, col: ColumnDimensionType) => {
      e.preventDefault()
      currentCol.value = null
      posY.value = e.clientY
      posX.value = e.clientX
      nextTick(() => {
        currentCol.value = col
      })
    }

    return {
      GridMode,
      mode,
      activeSheet,
      firstHeaderClass,
      getHeaderClass,
      getHeaderStyle,
      currentCol,
      posX,
      posY,
      showMenu
    }
  }
})
</script>
