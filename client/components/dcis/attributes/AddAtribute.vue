<template lang="pug">

</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { PeriodType } from '~/types/graphql'

export default defineComponent({
  period: { type: Object as PropType<PeriodType>, required: true }
})
</script>
