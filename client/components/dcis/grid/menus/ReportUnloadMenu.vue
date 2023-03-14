<template lang="pug">
v-menu(v-model="active" offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.reportUnloadMenu.buttonText') }}
  v-list(dense)
    slot(name="documents-filter" :title="$t('dcis.grid.sheetMenu.reportUnloadMenu.documentFilter')")
    slot(name="rows-filter" :title="$t('dcis.grid.sheetMenu.reportUnloadMenu.rowsFilter')")
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'

export default defineComponent({
  setup (_, { emit }) {
    const active = ref<boolean>(false)

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, close }
  }
})
</script>
