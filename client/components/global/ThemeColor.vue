<template lang="pug">
  v-dialog(v-model="active" width="600")
    template(#activator="{ on }")
      slot(:on="on")
    v-card
      v-card-title {{ $t('index.theme.change') }}
        v-spacer
        v-btn(@click="active = false" icon)
          v-icon mdi-close
      v-card-text
        v-row.text-center
          v-col(cols="12")
            v-btn-toggle(v-model="$colorMode.preference" tile mandatory)
              v-btn(v-for="theme in themes" :key="theme.value" :value="theme.value")
                | {{ $t(`index.theme.${theme.value}`) }}
                v-icon(right) mdi-{{ theme.icon }}
          v-col(cols="12") {{ $t('index.theme.selected', { theme: $t(`index.theme.${$colorMode.preference}`) }) }}
        v-row.text-center(v-if="$colorMode.preference === 'system'")
          v-col {{ $t('index.theme.detected', { theme: $t(`index.theme.${$colorMode.value}`) }) }}
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend<any, any, any, any>({
  data: () => ({
    active: false
  }),
  computed: {
    themes (): { value: string, icon: string }[] {
      return [
        { value: 'system', icon: 'desktop-classic' },
        { value: 'light', icon: 'lightbulb-on-outline' },
        { value: 'dark', icon: 'lightbulb-on' }
      ]
    }
  }
})
</script>
