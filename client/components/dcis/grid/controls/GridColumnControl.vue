<template lang="pug">
v-menu(:value="true" :position-x="posX" :position-y="posY" absolute close-on-content-click)
  template(#activator="{ on, attrs }")
    slot(:on="on" :attrs="attrs")
  v-list(dense)
    grid-column-settings(
      :column="column"
      :get-column-width="getColumnWidth"
      @close="$emit('close')"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-cog
          v-list-item-content
            v-list-item-title {{ $t('dcis.grid.columnControl.properties') }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { ColumnDimensionType } from '~/types/graphql'
import GridColumnSettings from '~/components/dcis/grid/settings/GridColumnSettings.vue'

export default defineComponent({
  components: { GridColumnSettings },
  props: {
    column: { type: Object as PropType<ColumnDimensionType>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true },
    posX: { type: Number, required: true },
    posY: { type: Number, required: true }
  }
})
</script>
