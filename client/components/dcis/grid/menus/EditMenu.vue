<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.editMenu.buttonText') }}
  v-list(dense width="200")
    v-list-item(@click="copy" :disabled="copyPasteDisabled")
      v-list-item-title.d-flex.justify-space-between
        span {{ $t('dcis.grid.sheetMenu.editMenu.copy') }}
        span {{ $t('dcis.grid.sheetMenu.editMenu.copyShortcut') }}
    v-list-item(v-if="pasteVisible" :disabled="copyPasteDisabled" @click="paste")
      v-list-item-title.d-flex.justify-space-between
        span {{ $t('dcis.grid.sheetMenu.editMenu.paste') }}
        span {{ $t('dcis.grid.sheetMenu.editMenu.pasteShortcut') }}
</template>

<script lang="ts">
import { defineComponent, PropType, computed } from '#app'
import { CellsOptionsType, GridMode } from '~/types/grid'

export default defineComponent({
  props: {
    mode: { type: Number as PropType<GridMode>, required: true },
    selectedCellsOptions: { type: Object as PropType<CellsOptionsType>, default: null }
  },
  setup (props) {
    const copyPasteDisabled = computed(() => !props.selectedCellsOptions)

    const copy = () => {
      /// Несмотря на статус `deprecated`, работает лучше современного варианта с navigator.clipboard.
      /// navigator.clipboard.write не работает в Firefox без установки специальных разрешений.
      document.execCommand('copy')
    }

    const pasteVisible = computed(() => props.mode === GridMode.WRITE || props.mode === GridMode.CHANGE)
    const paste = () => {
      const event = new Event('paste')
      document.dispatchEvent(event)
    }

    return {
      copyPasteDisabled,
      GridMode,
      copy,
      pasteVisible,
      paste
    }
  }
})
</script>
