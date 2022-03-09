<template lang="pug">
  v-menu(v-model="active" :close-on-content-click="false" bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-date-picker(v-model="date" @change="update")
</template>

<script lang="ts">
import type { Ref, SetupContext } from '#app'
import { defineComponent, toRef, ref } from '#app'

export default defineComponent({
  props: {
    value: { type: String, required: true }
  },
  setup (props, { emit }: SetupContext) {
    const date: Ref<string | null> = ref<string | null>(props.value)
    const active: Ref<boolean> = ref<boolean>(false)

    const update = () => {
      active.value = false
      if (date.value === null || date.value.length < 2) {
        date.value = props.value
      }
      emit('update', date.value)
    }

    return { date, active, update }
  }
})
</script>
