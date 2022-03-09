<template lang="pug">
  v-menu(v-model="active" :close-on-content-click="false" bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-card
      v-card-text
        v-select(v-model="lValue" v-bind="$attrs")
          template(v-slot:append-outer)
            v-btn(color="success" icon @click="update")
              v-icon mdi-check
</template>

<script lang="ts">
import type { Ref, SetupContext } from '#app'
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    value: { type: String, required: true }
  },
  setup (props, { emit }: SetupContext) {
    const lValue: Ref<string | null> = ref<string | null>(props.value)
    const active: Ref<boolean> = ref<boolean>(false)

    const update = () => {
      active.value = false
      emit('update', lValue.value)
    }

    return { lValue, active, update }
  }
})
</script>
