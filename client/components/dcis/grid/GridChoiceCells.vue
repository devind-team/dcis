<template lang="pug">
v-snackbar(:value="gridChoice.active.value" timeout="-1") {{ gridChoice.text.value }}
  template(#action="{ attrs }")
    v-btn(@click="gridChoice.endChoice" v-bind="attrs" text) Выбрать
    v-btn(@click="gridChoice.cancel" v-bind="attrs" icon)
      v-icon mdi-close
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { GridChoiceType } from '~/composables/grid-choice'

export default defineComponent({
  props: {
    gridChoice: { type: Object as PropType<GridChoiceType>, required: true }
  }
})
</script>
