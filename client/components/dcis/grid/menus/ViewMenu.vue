<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.viewMenu.buttonText') }}
  v-list(dense width="200")
    v-list-item(v-if="value.isFullScreen" @click="setIsFullScreen(false)")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.viewMenu.normalMode') }}
    v-list-item(v-else @click="setIsFullScreen(true)")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.viewMenu.fullScreenMode') }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { onKeyStroke } from '@vueuse/core'

export type ViewType = {
  isFullScreen: boolean
}

export default defineComponent({
  props: {
    value: { type: Object as PropType<ViewType>, required: true }
  },
  setup (props, { emit }) {
    const setIsFullScreen = (isFullScreen: boolean) => {
      emit('input', { ...props.value, isFullScreen })
    }

    onKeyStroke('Escape', () => {
      setIsFullScreen(false)
    })

    return { setIsFullScreen }
  }
})
</script>
