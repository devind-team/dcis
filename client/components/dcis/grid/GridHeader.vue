<template lang="pug">
  thead
    tr
      th(:style="{ width: `${rowIndexColumnWidth}px` }")
        .grid__header-content
          .grid__select-all
      th(
        v-for="column in columns"
        :key="column.columnDimension.id"
        :style="column.style"
      )
</template>

<script lang="ts">
import type { PropType } from '#app'
import { BuildColumnType } from '~/types/grid'

export default defineComponent({
  props: {
    rowIndexColumnWidth: { type: Number, required: true },
    columns: { type: Array as PropType<BuildColumnType[]>, required: true }
  }
})
</script>
