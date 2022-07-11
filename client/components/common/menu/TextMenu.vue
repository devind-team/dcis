<template lang="pug">
v-menu(v-model="active" :close-on-content-click="false" bottom)
  template(#activator="{ on }")
    slot(:on="on")
  v-card
    v-card-text
      v-textarea(v-if="multiline" v-model="text" clearable)
        template(v-slot:append-outer)
          v-btn(color="success" icon @click="update")
            v-icon mdi-check
      v-text-field(v-else v-model="text" clearable @keyup.enter="update")
        template(v-slot:append-outer)
          v-btn(color="success" icon @click="update")
            v-icon mdi-check
</template>

<script lang="ts">
import type { Ref, SetupContext } from '#app'
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    value: { type: String, required: true },
    multiline: { type: Boolean, default: false }
  },
  setup (props, { emit }: SetupContext) {
    const text: Ref<string | null> = ref<string | null>(props.value)
    const active: Ref<boolean> = ref<boolean>(false)

    const update = () => {
      active.value = false
      if (text.value === null || text.value.length < 2) {
        text.value = props.value
      }
      emit('update', text.value)
    }

    return { text, active, update }
  }
})
</script>
