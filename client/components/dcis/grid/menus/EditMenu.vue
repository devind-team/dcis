<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.editMenu.buttonText') }}
  v-dialog(v-model="shortcutDialogActive" width="570")
    v-card
      v-card-title
        | {{ $t('dcis.grid.sheetMenu.editMenu.shortcutDialog.title') }}
        v-spacer
        v-btn(@click="shortcutDialogActive = false" icon)
          v-icon mdi-close
      v-card-text
        span {{ $t('dcis.grid.sheetMenu.editMenu.shortcutDialog.message') }}
        .d-flex.mt-3
          .d-flex.flex-column.mr-7
            .text-h4 {{ $t('dcis.grid.sheetMenu.editMenu.cutShortcut') }}
            span {{ $t('dcis.grid.sheetMenu.editMenu.shortcutDialog.toCut') }}
          .d-flex.flex-column.mr-7
            .text-h4 {{ $t('dcis.grid.sheetMenu.editMenu.copyShortcut') }}
            span {{ $t('dcis.grid.sheetMenu.editMenu.shortcutDialog.toCopy') }}
          .d-flex.flex-column
            .text-h4 {{ $t('dcis.grid.sheetMenu.editMenu.pasteShortcut') }}
            span {{ $t('dcis.grid.sheetMenu.editMenu.shortcutDialog.toPaste') }}
  v-list(dense width="200")
    v-list-item(v-if="changeVisible" :disabled="disabled" @click="cut")
      v-list-item-title.d-flex.justify-space-between
        span {{ $t('dcis.grid.sheetMenu.editMenu.cut') }}
        span {{ $t('dcis.grid.sheetMenu.editMenu.cutShortcut') }}
    v-list-item(:disabled="disabled" @click="copy")
      v-list-item-title.d-flex.justify-space-between
        span {{ $t('dcis.grid.sheetMenu.editMenu.copy') }}
        span {{ $t('dcis.grid.sheetMenu.editMenu.copyShortcut') }}
    v-list-item(v-if="changeVisible" :disabled="disabled" @click.stop="paste")
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
    const shortcutDialogActive = ref(false)

    const disabled = computed(() => !props.selectedCellsOptions)
    const changeVisible = computed(() => props.mode === GridMode.WRITE || props.mode === GridMode.CHANGE)

    const cut = () => {
      /// Несмотря на статус `deprecated`, работает лучше современного варианта с navigator.clipboard.
      /// navigator.clipboard.write не работает в Firefox без установки специальных разрешений.
      document.execCommand('cut')
    }

    const copy = () => {
      document.execCommand('copy')
    }

    const paste = () => {
      if (!navigator.clipboard.readText || !navigator.clipboard.read) {
        shortcutDialogActive.value = true
      } else {
        const event = new Event('paste')
        document.dispatchEvent(event)
      }
    }

    return {
      shortcutDialogActive,
      disabled,
      GridMode,
      changeVisible,
      cut,
      copy,
      paste
    }
  }
})
</script>
