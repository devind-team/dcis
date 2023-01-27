<template lang="pug">
v-menu(:value="true" :position-x="posX" :position-y="posY" absolute close-on-content-click)
  template(#activator="{ on, attrs }")
    slot(:on="on" :attrs="attrs")
  v-list(dense)
    component(
      :is="settingsComponent"
      :column="column"
      :get-column-width="getColumnWidth"
      @submit="({ width }) => changeColumnWidth(column, width)"
      @reset="resetColumnWidth(column)"
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
import { computed, inject, PropType } from '#app'
import { ColumnDimensionType } from '~/types/graphql'
import { GridMode, GridModeInject } from '~/types/grid'
import GridColumnSettings from '~/components/dcis/grid/settings/GridColumnSettings.vue'
import GridColumnLocalSettings from '~/components/dcis/grid/settings/GridColumnLocalSettings.vue'

export default defineComponent({
  components: { GridColumnSettings, GridColumnLocalSettings },
  props: {
    column: { type: Object as PropType<ColumnDimensionType>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true },
    changeColumnWidth: {
      type: Function as PropType<(columnDimension: ColumnDimensionType, width: number) => void>,
      required: true
    },
    resetColumnWidth: { type: Function as PropType<(columnDimension: ColumnDimensionType) => void>, required: true },
    posX: { type: Number, required: true },
    posY: { type: Number, required: true }
  },
  setup () {
    const mode = inject(GridModeInject)

    const settingsComponent = computed<string>(
      () => mode.value === GridMode.CHANGE ? 'GridColumnSettings' : 'GridColumnLocalSettings'
    )

    return { settingsComponent }
  }
})
</script>
