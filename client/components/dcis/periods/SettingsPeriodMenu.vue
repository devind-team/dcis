<template lang="pug">
v-menu(v-model="active" origin="center center" transition="scale-transition")
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attr="attrs")
  v-list
    change-show-sheets(v-slot="{ on, attrs }" @close="active = false" :sheets="sheets")
      v-list-item(v-on="on" v-bind="attrs")
        v-list-item-icon
          v-icon mdi-checkbox-blank-off
        v-list-item-content {{ $t('dcis.sheets.settings.show') }}
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
  setup () {
    const active = ref<boolean>(false)

    return { active }
  }
})
</script>
