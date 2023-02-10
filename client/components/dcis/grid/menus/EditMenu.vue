<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.editMenu.buttonText') }}
  v-list(dense)
    v-list-item
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.copy') }}
    v-list-item
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.copyWithStyles') }}
    v-list-item(v-if="mode === GridMode.WRITE || mode === GridMode.CHANGE")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.paste') }}
    v-list-item(v-if="mode === GridMode.CHANGE")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.pasteWithStyles') }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { GridMode } from '~/types/grid'

export default defineComponent({
  props: {
    mode: { type: Number as PropType<GridMode>, required: true }
  },
  setup () {
    return { GridMode }
  }
})
</script>
