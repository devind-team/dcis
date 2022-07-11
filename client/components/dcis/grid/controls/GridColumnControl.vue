<template lang="pug">
v-menu(v-model="active" bottom close-on-content-click)
  template(#activator="{ on, attrs }")
    slot(:on="on" :attrs="attrs")
  v-list(dense)
    grid-column-settings(
      :column="column"
      :get-column-width="getColumnWidth"
      @close="active = false"
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
import { ColumnDimensionType } from '~/types/graphql'
import GridColumnSettings from '~/components/dcis/grid/settings/GridColumnSettings.vue'

export default defineComponent({
  components: { GridColumnSettings },
  props: {
    column: { type: Object as PropType<ColumnDimensionType>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true }
  },
  setup () {
    const { t } = useI18n()

    const active = ref<boolean>(false)

    return { t, active }
  }
})
</script>
