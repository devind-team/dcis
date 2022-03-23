<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    v-card
      v-card-title Изменение значения
        v-spacer
        v-btn(@click="cancel" icon)
          v-icon mdi-close
      v-card-text
        v-textarea(v-model="rawValue" auto-grow autofocus)
      v-card-actions
        v-btn(@click="cancel") {{ $t('cancel') }}
        v-spacer
        v-btn(@click="setValue" color="primary") {{ $t('save') }}
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    value: { type: String, default: null }
  },
  setup (props, { emit }) {
    const active: Ref<boolean> = ref<boolean>(true)
    const rawValue: Ref<string> = ref<string>(props.value)

    const setValue = () => {
      active.value = false
      emit('set-value', rawValue.value)
    }

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    return { active, rawValue, setValue, cancel }
  }
})
</script>
