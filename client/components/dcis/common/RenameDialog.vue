<template lang="pug">
  v-dialog(v-model="active" width="400")
    template(#activator="{ on, attrs }")
      slot(:on="on" :attrs="attrs")
    v-card
      v-card-title {{ label }}
      v-card-subtitle {{ n }}
      v-card-text
        v-text-field(v-model="current")
      v-card-actions
        v-btn(@click="close") {{ $t('cancel') }}
        v-spacer
        v-btn(@click="apply" color="primary") {{ $t('apply') }}
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    n: { type: String, required: true },
    label: { type: String, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)
    const current = ref<string>(props.n)

    const close = () => {
      active.value = false
      emit('close')
    }

    const apply = () => {
      close()
      emit('apply', current.value)
    }

    return { active, current, close, apply }
  }
})
</script>
