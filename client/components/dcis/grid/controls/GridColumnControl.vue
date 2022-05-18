<template lang="pug">
  v-menu(v-model="settingsActive" bottom close-on-content-click)
    template(#activator="{ on, attrs }")
      slot(:on="on" :attrs="attrs")
    v-list(dense)
      grid-column-settings(
        :buildColumn="buildColumn"
        :get-column-width="getColumnWidth"
        @close="settingsActive = false"
      )
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-cog
            v-list-item-content
              v-list-item-title {{ t('dcis.grid.columnControl.properties') }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { BuildColumnType } from '~/types/grid'
import GridColumnSettings from '~/components/dcis/grid/settings/GridColumnSettings.vue'

export default defineComponent({
  components: { GridColumnSettings },
  props: {
    buildColumn: { type: Object as PropType<BuildColumnType>, required: true },
    getColumnWidth: { type: Function as PropType<(buildColumn: BuildColumnType) => number>, required: true }
  },
  setup () {
    const { t } = useI18n()

    const settingsActive = ref<boolean>(false)

    return { t, settingsActive }
  }
})
</script>
