<template lang="pug">
html
  body
    table
      tbody
        tr(v-for="row in selectedCells")
          td(v-for="cell in row" :colspan="cell.colspan" :rowspan="cell.rowspan") {{ cell.value }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { CellType } from '~/types/graphql'

export default defineComponent({
  props: {
    selectedCells: { type: Array as PropType<CellType[][]>, required: true }
  }
})
</script>
