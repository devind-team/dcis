<template lang="pug">
  div User {{ value }}
</template>

<script lang="ts">
import { defineComponent } from '#app'

export default defineComponent({
  props: {
    value: { type: String, default: null }
  }
})
</script>
