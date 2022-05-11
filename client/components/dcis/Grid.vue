<template lang="pug">
  div
    pre {{ columns }}
    pre {{ rows }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { SheetType } from '~/types/graphql'

export default defineComponent({
  props: {
    sheet: { type: Object as PropType<SheetType>, required: true }
  },
  setup (props) {
    const sheet = toRef(props, 'sheet')
    const {
      columns,
      rows
    } = useGrid(sheet)

    return { columns, rows }
  }
})
</script>
