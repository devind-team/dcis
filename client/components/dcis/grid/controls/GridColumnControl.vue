<template lang="pug">
  v-menu(v-model="active" bottom close-on-content-click)
    template(#activator="{ on, attrs }")
      slot(:on="on" :attrs="attrs")
    v-list(dense)
      column-settings(@close="active = false" :column="column")
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-cog
            v-list-item-content
              v-list-item-title Свойства
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent, ref } from '#app'
import { BuildColumnType } from '~/types/grid-types'
import ColumnSettings from '~/components/dcis/documents/ColumnSettings.vue'

export default defineComponent({
  components: { ColumnSettings },
  props: {
    column: { type: Object as PropType<BuildColumnType>, required: true }
  },
  setup () {
    const active = ref<boolean>(false)

    return { active }
  }
})
</script>
