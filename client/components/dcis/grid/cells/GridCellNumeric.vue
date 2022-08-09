<template lang="pug">
input(
  v-focus
  :value="value"
  type="number"
  @keyup.esc="$emit('cancel')"
  @keyup.enter="$event.target.blur()"
  @keyup.tab.stop="$event.target.blur()"
  @blur="$emit('set-value', $event.target.value)"
)
</template>

<script lang="ts">
export default defineComponent({
  directives: {
    focus: {
      inserted (el) {
        el.focus()
      }
    }
  },
  props: {
    value: { type: Number, default: null }
  }
})
</script>
