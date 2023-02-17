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
    v-list-item(@click="copy")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.copy') }}
    v-list-item(@click="copyWithStyles")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.copyWithStyles') }}
    v-list-item(v-if="mode === GridMode.WRITE || mode === GridMode.CHANGE" @click="paste")
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
    const copy = () => {
      const event = new Event('copy')
      document.dispatchEvent(event)
    }

    const copyWithStyles = () => {
      const event = new CustomEvent('copy-with-styles')
      document.dispatchEvent(event)
    }

    const paste = () => {
      const event = new Event('paste')
      document.dispatchEvent(event)
    }

    return { GridMode, copy, copyWithStyles, paste }
  }
})
</script>
