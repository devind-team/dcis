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
        grid-column-control(v-slot="{ on, attrs }" :column="column")
          div(
            v-bind="attrs"
            @contextmenu.prevent="on.click"
            :class="getHeaderContentClasses(column)"
          ) {{ column.columnDimension.index }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildColumnType } from '~/types/grid'
import GridColumnControl from '~/components/dcis/grid/controls/GridColumnControl.vue'

export default defineComponent({
  components: { GridColumnControl },
  props: {
    rowIndexColumnWidth: { type: Number, required: true },
    columns: { type: Array as PropType<BuildColumnType[]>, required: true },
    selectedColumnPositions: { type: Array as PropType<number[]>, required: true }
  },
  setup (props) {
    const getHeaderContentClasses = (column: BuildColumnType): (string | Record<string, boolean>)[] => {
      return [
        'grid__header-content',
        { 'grid__header-content_selected': props.selectedColumnPositions.includes(column.columnDimension.index) }
      ]
    }
    return {
      getHeaderContentClasses
    }
  }
})
</script>
