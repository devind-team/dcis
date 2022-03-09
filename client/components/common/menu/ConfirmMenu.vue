<template lang="pug">
  v-menu(v-model="active" bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-card
      v-card-text {{ text }}
      v-card-actions
        v-btn(:color="yesColor" @click="confirm") {{ $t('common.menu.confirmMenu.yes') }}
        v-spacer
        v-btn(:color="noColor" @click="cancel") {{ $t('common.menu.confirmMenu.no') }}
</template>

<script lang="ts">
import type { Ref, SetupContext } from '#app'
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    text: { type: String, required: true },
    yesColor: { type: String, required: true },
    noColor: { type: String, required: true }
  },
  setup (_, { emit }: SetupContext) {
    const active: Ref<boolean> = ref<boolean>(false)

    const confirm = () => {
      active.value = false
      emit('confirm')
    }

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    return { active, confirm, cancel }
  }
})
</script>
