<template lang="pug">
  thead
    tr
      th(:style="{ width: `${rowIndexColumnWidth}px` }")
        .grid__header-content.grid__row-index-header-content(:class="contentClass")
      th(
        v-for="column in columns"
        :key="column.id"
        :style="column.style"
        @mousemove="moveColumnHeader($event, column)"
        @mouseleave="leaveColumnHeader"
        @mousedown="startColumnResizing"
        @mouseup="endColumnResizing"
      )
        .grid__header-content(:class="contentClass") {{ column.position }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { BuildColumnType } from '~/types/grid-types'

export default defineComponent({
  props: {
    rowIndexColumnWidth: { type: Number, required: true },
    columns: { type: Array as PropType<BuildColumnType[]>, required: true },
    moveColumnHeader: {
      type: Function as PropType<(event: MouseEvent, column: BuildColumnType) => void>,
      required: true
    },
    leaveColumnHeader: { type: Function as PropType<() => void>, required: true },
    startColumnResizing: { type: Function as PropType<(event: MouseEvent) => void>, required: true },
    endColumnResizing: { type: Function as PropType<() => void>, required: true },
    scrollTop: { type: Number, required: true }
  },
  setup (props) {
    const contentClass = computed(() => ({
      'grid__header-content_bottom-border': props.scrollTop > 0
    }))
    return {
      contentClass
    }
  }
})
</script>
