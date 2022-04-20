<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    v-card
      v-card-title {{ t('dcis.cells.gridCellFile.title') }}
        v-spacer
        v-btn(@click="cancel" icon)
          v-icon mdi-close
      v-card-text
        file-field(
          v-model="rawValue"
          :label="t('dcis.cells.gridCellFile.label')"
          :existing-file="{ name: value, src: value }"
        )
      v-card-actions
        v-spacer
        v-btn(@click="setValue" color="primary") {{ t('save') }}
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import { useI18n } from '~/composables'
import FileField from '~/components/common/FileField.vue'

export default defineComponent({
  components: { FileField },
  props: {
    value: { type: String, default: null }
  },
  setup (_, { emit }) {
    const { t } = useI18n()

    const active = ref<boolean>(true)
    const rawValue = ref<string>(null)

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
