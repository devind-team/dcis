<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    v-card
      v-card-title {{ t('dcis.grid.cellText.title') }}
        v-spacer
        v-btn(@click="cancel" icon)
          v-icon mdi-close
      v-card-text
        v-textarea(v-model="rawValue" auto-grow autofocus)
      v-card-actions
        v-spacer
        v-btn(@click="setValue" color="primary") {{ $t('save') }}
</template>

<script lang="ts">
export default defineComponent({
  props: {
    value: { type: String, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const active = ref<boolean>(true)
    const rawValue = ref<string>(props.value)

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    const setValue = () => {
      active.value = false
      emit('set-value', rawValue.value)
    }

    return { t, active, rawValue, setValue, cancel }
  }
})
</script>
