<template lang="pug">
  thead
    tr
      th(:style="{ width: `${rowIndexColumnWidth}px` }")
        .grid__header-content
      th(
        v-for="column in columns"
        :key="column.id"
        :style="column.style"
        @mousemove="moveColumnHeader($event, column)"
        @mouseleave="leaveColumnHeader"
        @mousedown="startColumnResizing"
        @mouseup="endColumnResizing"
      )
        div(:class="getHeaderContentClasses(column)") {{ column.position }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { BuildColumnType, BoundaryRowCell } from '~/types/grid-types'

export default defineComponent({
  props: {
    rowIndexColumnWidth: { type: Number, required: true },
    columns: { type: Array as PropType<BuildColumnType[]>, required: true },
    selectionColumns: { type: Array as PropType<number[]>, required: true },
    selectedBoundaryRowCells: { type: Array as PropType<BoundaryRowCell[]>, required: true },
    moveColumnHeader: {
      type: Function as PropType<(event: MouseEvent, column: BuildColumnType) => void>,
      required: true
    },
    leaveColumnHeader: { type: Function as PropType<() => void>, required: true },
    startColumnResizing: { type: Function as PropType<(event: MouseEvent) => void>, required: true },
    endColumnResizing: { type: Function as PropType<() => void>, required: true }
  },
  setup (props) {
    const getHeaderContentClasses = (column: BuildColumnType): (string | Record<string, boolean>)[] => {
      return [
        'grid__header-content',
        { 'grid__header-content_selected': props.selectionColumns.includes(column.index) },
        {
          'grid__header-content_neighbor-selected':
            !!props.selectedBoundaryRowCells.find(boundaryCell =>
              boundaryCell.columns.find(boundaryRowCell => boundaryRowCell.id === column.id))
        }
      ]
    }
    return {
      getHeaderContentClasses
    }
  }
})
</script>
