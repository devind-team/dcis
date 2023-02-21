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
    v-list-item(@click="copy" :disabled="copyDisabled")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.copy') }}
    v-list-item(@click="copyWithStyles" :disabled="copyDisabled")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.copyWithStyles') }}
    v-list-item(v-if="pasteVisible" @click="paste")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.paste') }}
    v-list-item(v-if="pasteWithStylesVisible" @click="pasteWithStyles")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.editMenu.pasteWithStyles') }}
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
    const copyDisabled = computed(() => !props.selectedCellsOptions)

    const copy = () => {
      const event = new Event('copy')
      document.dispatchEvent(event)
    }

    const copyWithStyles = () => {
      const event = new CustomEvent('copy-with-styles')
      document.dispatchEvent(event)
    }

    const pasteVisible = computed(() => props.mode === GridMode.WRITE || props.mode === GridMode.CHANGE)
    const paste = () => {
      const event = new Event('paste')
      document.dispatchEvent(event)
    }

    const pasteWithStylesVisible = computed(() => props.mode === GridMode.CHANGE)
    const pasteWithStyles = () => {
      const event = new CustomEvent('paste-with-styles')
      document.dispatchEvent(event)
    }

    return {
      copyDisabled,
      GridMode,
      copy,
      copyWithStyles,
      pasteVisible,
      paste,
      pasteWithStylesVisible,
      pasteWithStyles
    }
  }
})
</script>
