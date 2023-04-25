<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.scanMenu.buttonText') }}
  v-list(dense width="200")
    v-list-item
      v-list-item-title.d-flex.justify-space-between {{ $t('dcis.grid.sheetMenu.scanMenu.uploadScan') }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { DocumentType } from '~/types/graphql'

export default defineComponent({
  props: { document: { type: Object as PropType<DocumentType>, required: true } },
  setup(props) {
    return
  }
})
</script>

<style scoped>

</style>
