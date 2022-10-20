<template lang="pug">
v-dialog(v-model="active" width="650px")
  template(#activator="{ on }")
    div(v-on="on") {{ value }}
  v-card
    v-card-title {{ t('dcis.grid.changeValue') }}
      v-spacer
      v-btn(@click="cancel" icon)
        v-icon mdi-close
    v-card-text Основной контекнт
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  props: {
    value: { type: String, default: null }
  },
  setup (_, { emit }) {
    const { t } = useI18n()
    const active = ref<boolean>(true)

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    return { active, cancel, t }
  }
})
</script>
