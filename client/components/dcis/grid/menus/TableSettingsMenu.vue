<template lang="pug">
v-menu(v-model="active" offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.tableSettings.buttonText') }}
  v-list(dense)
    change-show-sheets(v-slot="{ on, attrs }" :sheets="sheets" @close="close")
      v-list-item(v-on="on" v-bind="attrs")
        v-list-item-title {{ $t('dcis.grid.sheetMenu.tableSettings.showSettings') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import ChangeShowSheets from '~/components/dcis/periods/ChangeShowSheets.vue'
import { BaseSheetType } from '~/types/graphql'

export default defineComponent({
  components: { ChangeShowSheets },
  props: {
    sheets: { type: Array as PropType<BaseSheetType[]>, required: true }
  },
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
