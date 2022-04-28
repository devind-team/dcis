<template lang="pug">
  v-menu(v-model="active" bottom close-on-content-click)
    template(#activator="{ on, attrs }")
      slot(:on="on" :attrs="attrs")
    v-list(dense)
      grid-column-settings(@close="active = false" :column="column")
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-cog
            v-list-item-content
              v-list-item-title {{ t('dcis.grid.columnControl.properties') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import type { BuildColumnType } from '~/types/grid-types'
import GridColumnSettings from '~/components/dcis/grid/GridColumnSettings.vue'

export default defineComponent({
  components: { GridColumnSettings },
  props: {
    column: { type: Object as PropType<BuildColumnType>, required: true }
  },
  setup () {
    const { t } = useI18n()

    const active = ref<boolean>(false)

    return { t, active }
  }
})
</script>
