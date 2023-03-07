<template lang="pug">
header.grid-sheet-menu__header
  slot
</template>

<script lang="ts">
import { defineComponent } from '#app'

export default defineComponent({})
</script>

<style lang="sass">
.grid-sheet-menu__header
  height: 36px
.grid-sheet-menu__button
  padding-left: 8px !important
  padding-right: 8px !important
  text-transform: none
</style>
