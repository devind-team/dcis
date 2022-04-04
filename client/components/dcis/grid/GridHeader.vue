<template lang="pug">
  thead
    tr
      th(style="width: 30px")
      th(
        v-for="column in columns"
        :key="column.id"
        :style="column.style"
        @mousemove="moveColumnHeader($event, column.index)"
        @mouseleave="leaveColumnHeader"
        @mousedown="startColumnResizing"
        @mouseup="endColumnResizing"
      ) {{ column.positional }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { BuildColumnType } from '~/types/grid-types'

export default defineComponent({
  props: {
    columns: { type: Array as PropType<BuildColumnType[]>, required: true },
    moveColumnHeader: { type: Function as PropType<(e: MouseEvent, index: number) => void>, required: true },
    leaveColumnHeader: { type: Function as PropType<() => void>, required: true },
    startColumnResizing: { type: Function as PropType<() => void>, required: true },
    endColumnResizing: { type: Function as PropType<() => void>, required: true }
  }
})
</script>
