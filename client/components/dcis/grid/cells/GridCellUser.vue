<template lang="pug">
  div User {{ value }}
</template>

<script lang="ts">
export default defineComponent({
  props: {
    value: { type: String, default: null }
  }
})
</script>
