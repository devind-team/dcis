<template lang="pug">
v-dialog(v-model="active" width="800")
  template(#activator="{ on }")
    slot(:on="on")
  v-card
    v-card-title {{ text }}
      v-spacer
      v-btn(@click="close" icon)
        v-icon mdi-close
    v-card-text Вывод инструкции в переработке! [{{ doc }}]
</template>

<script lang="ts">
import type { Ref, SetupContext } from '#app'
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    doc: { type: String, required: true },
    text: { type: String, required: true }
  },
  setup (_, { emit }: SetupContext) {
    const active: Ref<boolean> = ref<boolean>(false)

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, close }
  }
})
</script>
