<template lang="pug">
  input(
    v-focus
    @keyup.esc="$emit('cancel')"
    @keyup.enter="$event.target.blur()"
    @keyup.tab.stop="$event.target.blur()"
    @blur="setValue($event.target.value)"
    :value="value"
    type="text"
  )
</template>

<script lang="ts">
import accounting from 'accounting'

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
  },
  setup (_, { emit }) {
    const setValue = (value: string) => {
      if (value) {
        const money: string = value.replace(',', '.')
        emit('set-value', accounting.formatNumber(money, 2, ' ', ','))
      } else {
        emit('set-value', value)
      }
    }
    return { setValue }
  }
})
</script>
