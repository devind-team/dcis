<template lang="pug">
  input(
    v-focus
    @keyup.esc="$emit('cancel')"
    @keyup.enter="$event.target.blur()"
    @keyup.tab.stop="$event.target.blur()"
    @blur="$emit('set-value', $event.target.value)"
    :value="value"
    type="number"
  )
</template>

<script lang="ts">
import { defineComponent } from '#app'

export default defineComponent({
  directives: {
    focus: {
      inserted (el) {
        el.focus()
      }
    }
  },
  props: {
    value: { type: String, default: null }
  }
})
</script>
