<template lang="pug">
v-menu(:value="true" :position-x="posX" :position-y="posY" absolute close-on-content-click)
  v-list(dense)
    grid-row-settings(
      v-if="canChangeSettings"
      :row="row"
      :get-row-height="getRowHeight"
      @close="$emit('close')"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-cog
          v-list-item-content {{ t('dcis.grid.rowControl.properties') }}
    v-list-item(v-if="canAddBefore" @click="addRowDimensionMutate(row, AddRowDimensionPosition.BEFORE)")
      v-list-item-icon
        v-icon mdi-table-row-plus-before
      v-list-item-content {{ t('dcis.grid.rowControl.addRowAbove') }}
    v-list-item(v-if="canAddAfter" @click="addRowDimensionMutate(row, AddRowDimensionPosition.AFTER)")
      v-list-item-icon
        v-icon mdi-table-row-plus-after
      v-list-item-content {{ t('dcis.grid.rowControl.addRowBelow') }}
    v-list-item(
      v-if="canAddInside"
      @click="addRowDimensionMutate(row, AddRowDimensionPosition.INSIDE)"
    )
      v-list-item-icon
        v-icon mdi-table-row-plus-after
      v-list-item-content {{ t('dcis.grid.rowControl.addChildRow') }}
    v-list-item(v-if="canDelete" @click="deleteRowDimension(row)")
      v-list-item-icon
        v-icon(color="error") mdi-table-row-remove
      v-list-item-content(color="error") {{ t('dcis.grid.rowControl.deleteRow') }}
</template>

<script lang="ts">
import { PropType, Ref } from '#app'
import { AddRowDimensionPosition, UpdateType } from '~/composables'
import { GridMode, UpdateSheetType } from '~/types/grid'
import { DocumentSheetQuery, DocumentsSheetQuery, DocumentType, RowDimensionType, SheetType } from '~/types/graphql'
import GridRowSettings from '~/components/dcis/grid/settings/GridRowSettings.vue'

export default defineComponent({
  components: { GridRowSettings },
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    canChangeSettings: { type: Boolean, required: true },
    canAddBefore: { type: Boolean, required: true },
    canAddAfter: { type: Boolean, required: true },
    canAddInside: { type: Boolean, required: true },
    canDelete: { type: Boolean, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
    clearSelection: { type: Function as PropType<() => void>, required: true },
    posX: { type: Number, required: true },
    posY: { type: Number, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const mode = inject<GridMode>('mode')
    const activeDocument = inject<Ref<DocumentType | null>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateSheetType>>('updateActiveSheet')

    const addRowDimensionMutate = mode === GridMode.CHANGE
      ? useAddRowDimensionMutation(
        activeSheet,
        updateSheet as Ref<UpdateType<DocumentsSheetQuery>>
      )
      : useAddChildRowDimensionMutation(
        computed(() => activeDocument.value ? activeDocument.value.id : null),
        activeSheet,
        updateSheet as Ref<UpdateType<DocumentSheetQuery>>
      )

    const deleteRowDimensionMutate = mode === GridMode.CHANGE
      ? useDeleteRowDimensionMutation(activeSheet, updateSheet as Ref<UpdateType<DocumentsSheetQuery>>)
      : useDeleteChildRowDimensionMutation(activeSheet, updateSheet as Ref<UpdateType<DocumentSheetQuery>>)

    const deleteRowDimension = async (row: RowDimensionType) => {
      await deleteRowDimensionMutate(row)
      props.clearSelection()
    }

    return {
      AddRowDimensionPosition,
      t,
      addRowDimensionMutate,
      deleteRowDimension
    }
  }
})
</script>
