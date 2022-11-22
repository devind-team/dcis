<template lang="pug">
v-menu(v-model="active" origin="center center" transition="scale-transition")
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attr="attrs")
  v-list
    v-list-item
      v-list-item-icon
        v-icon mdi-download
      v-list-item-content {{ $t('dcis.periods.report.settings.unload') }}
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'

export default defineComponent({
  setup () {
    const active = ref<boolean>(false)

    return { active }
  }
})
</script>
