<template lang="pug">
v-dialog(v-model="active" width="600")
  template(#activator="{ on }")
    slot(:on="on")
  v-card
    v-card-title {{ $t('common.dialogs.experimentalDialog.title') }}
      v-spacer
      v-btn(@click="active=false" icon)
        v-icon mdi-close
    v-card-subtitle {{ $t('common.dialogs.experimentalDialog.subtitle') }}
    v-card-text {{ $t('common.dialogs.experimentalDialog.text') }}
</template>

<script lang="ts">
import type { Ref } from '#app'
import { ref, defineComponent } from '#app'

export default defineComponent({
  setup () {
    const active: Ref<boolean> = ref<boolean>(false)
    return { active }
  }
})
</script>
