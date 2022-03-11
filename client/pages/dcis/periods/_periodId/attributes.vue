<template lang="pug">
  v-container(fluid)
    v-row it work
</template>

<script lang="ts">
import { defineComponent, useNuxt2Meta } from '#app'

export default defineComponent({
  middleware: 'auth',
  setup () {
    useNuxt2Meta({ title: 'Атрибуты' })
  }
})
</script>
