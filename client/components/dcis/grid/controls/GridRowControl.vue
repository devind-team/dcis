<template lang="pug">
v-menu(:value="true" :position-x="posX" :position-y="posY" absolute close-on-content-click)
  v-list(dense)
    component(
      :is="settingsComponent"
      :row="row"
      :get-row-height="getRowHeight"
      @submit="({ height }) => changeRowHeight(row, height)"
      @reset="resetRowHeight(row)"
      @close="$emit('close')"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-cog
          v-list-item-content {{ $t('dcis.grid.rowControl.properties') }}
    v-list-item(v-if="canAddBefore" @click="addRowDimension(row, AddRowDimensionPosition.BEFORE)")
      v-list-item-icon
        v-icon mdi-table-row-plus-before
      v-list-item-content {{ $t('dcis.grid.rowControl.addRowAbove') }}
    v-list-item(v-if="canAddAfter" @click="addRowDimension(row, AddRowDimensionPosition.AFTER)")
      v-list-item-icon
        v-icon mdi-table-row-plus-after
      v-list-item-content {{ $t('dcis.grid.rowControl.addRowBelow') }}
    v-list-item(
      v-if="canAddInside"
      @click="addRowDimension(row, AddRowDimensionPosition.INSIDE)"
    )
      v-list-item-icon
        v-icon mdi-table-row-plus-after
      v-list-item-content {{ $t('dcis.grid.rowControl.addChildRow') }}
    v-list-item(v-if="canDelete" @click="deleteRowDimension(row)")
      v-list-item-icon
        v-icon(color="error") mdi-table-row-remove
      v-list-item-content(color="error") {{ $t('dcis.grid.rowControl.deleteRow') }}
</template>

<script lang="ts">
import { computed, inject, PropType } from '#app'
import { AddRowDimensionPosition } from '~/composables/grid-mutations'
import { useAddRowDimension, useDeleteRowDimension } from '~/composables/grid-actions'
import { RowDimensionType } from '~/types/graphql'
import { GridMode, GridModeInject } from '~/types/grid'
import GridRowSettings from '~/components/dcis/grid/settings/GridRowSettings.vue'
import GridRowLocalSettings from '~/components/dcis/grid/settings/GridRowLocalSettings.vue'

export default defineComponent({
  components: { GridRowSettings, GridRowLocalSettings },
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    canAddBefore: { type: Boolean, required: true },
    canAddAfter: { type: Boolean, required: true },
    canAddInside: { type: Boolean, required: true },
    canDelete: { type: Boolean, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
    changeRowHeight: {
      type: Function as PropType<(rowDimension: RowDimensionType, height: number) => void>,
      required: true
    },
    resetRowHeight: { type: Function as PropType<(rowDimension: RowDimensionType) => void>, required: true },
    clearSelection: { type: Function as PropType<() => void>, required: true },
    posX: { type: Number, required: true },
    posY: { type: Number, required: true }
  },
  setup (props) {
    const mode = inject(GridModeInject)

    const settingsComponent = computed<string>(
      () => mode.value === GridMode.CHANGE ? 'GridRowSettings' : 'GridRowLocalSettings'
    )

    const addRowDimension = useAddRowDimension()
    const deleteRowDimensionMutate = useDeleteRowDimension()

    const deleteRowDimension = async (row: RowDimensionType) => {
      await deleteRowDimensionMutate(row)
      props.clearSelection()
    }

    return {
      AddRowDimensionPosition,
      settingsComponent,
      addRowDimension,
      deleteRowDimension
    }
  }
})
</script>
