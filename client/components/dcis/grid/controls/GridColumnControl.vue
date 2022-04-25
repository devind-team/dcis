<template lang="pug">
  v-menu(v-model="active" bottom close-on-content-click)
    template(#activator="{ on, attrs }")
      slot(:on="on" :attrs="attrs")
    v-list(dense)
      v-list-item(@click="")
        v-list-item-icon
          v-icon mdi-cog
        v-list-item-content
          v-list-item-title Свойства
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent, ref } from '#app'

export default defineComponent({
  props: {
    column: { type: Object as PropType<any>, required: true }
  },
  setup () {
    const active = ref<boolean>(false)

    return { active }
  }
})
</script>
