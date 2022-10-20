<template lang="pug">
v-dialog(v-model="active" width="600")
  template(#activator="{ on }")
    div(class="mr-1 v-item-group theme--light v-btn-toggle")
      slot(name="default" :on="on")
  v-card
    v-card-title Агрегация
      v-spacer
      v-btn(@click="cancel" icon)
        v-icon mdi-close
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { CellType } from '~/types/graphql'

export default defineComponent({
  props: {
    cell: { type: Object as PropType<CellType>, default: null }
  },
  setup (_, { emit }) {
    const active = ref<boolean>(false)
    const cancel = () => {
      emit('close')
      active.value = false
    }

    return { active, cancel }
  }
})
</script>
