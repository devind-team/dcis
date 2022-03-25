<template lang="pug">
  thead
    tr
      th(style="width: 30px")
      th(
        v-for="column in columns"
        :key="column.id"
        :style="column.style"
      ) {{ column.positional }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { BuildColumnType } from '~/types/grid-types'

export default defineComponent({
  props: {
    columns: { type: Array as PropType<BuildColumnType[]>, required: true }
  }
})
</script>
