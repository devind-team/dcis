<template lang="pug">
v-menu(v-model="active" bottom close-on-content-click)
  template(#activator="{ on, attrs }")
    slot(:on="on" :attrs="attrs")
  v-list(dense)
    grid-row-settings(
      v-if="mode === GridMode.CHANGE"
      :row="row"
      :get-row-height="getRowHeight"
      @close="active = false"
    )
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-cog
          v-list-item-content {{ t('dcis.grid.rowControl.properties') }}
    v-list-item(@click="addRowDimensionMutate(row, AddRowDimensionPosition.BEFORE)")
      v-list-item-icon
        v-icon mdi-table-row-plus-before
      v-list-item-content {{ t('dcis.grid.rowControl.addRowAbove') }}
    v-list-item(@click="addRowDimensionMutate(row, AddRowDimensionPosition.AFTER)")
      v-list-item-icon
        v-icon mdi-table-row-plus-after
      v-list-item-content {{ t('dcis.grid.rowControl.addRowBelow') }}
    v-list-item(
      v-if="row.dynamic"
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
import { GridMode, UpdateSheetType } from '~/types/grid'
import { DocumentType, RowDimensionType, SheetType, DocumentsSheetQuery, DocumentSheetQuery } from '~/types/graphql'
import { UpdateType } from '~/composables'
import { AddRowDimensionPosition } from '~/composables/grid-mutations'
import GridRowSettings from '~/components/dcis/grid/settings/GridRowSettings.vue'

export default defineComponent({
  components: { GridRowSettings },
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    canDelete: { type: Boolean, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true },
    clearSelection: { type: Function as PropType<() => void>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const active = ref<boolean>(false)

    const mode = inject<GridMode>('mode')
    const activeDocument = inject<Ref<DocumentType | null>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateSheetType>>('updateActiveSheet')

    const addRowDimensionMutate = useAddRowDimensionMutation(
      computed(() => activeDocument.value ? activeDocument.value.id : null),
      activeSheet,
      updateSheet
    )

    const deleteRowDimensionMutate = mode === GridMode.CHANGE
      ? useDeleteRowDimensionMutation(activeSheet, updateSheet as Ref<UpdateType<DocumentsSheetQuery>>)
      : useDeleteChildRowDimensionMutation(activeSheet, updateSheet as Ref<UpdateType<DocumentSheetQuery>>)

    const deleteRowDimension = async (row: RowDimensionType) => {
      await deleteRowDimensionMutate(row)
      props.clearSelection()
    }

    return {
      GridMode,
      t,
      mode,
      active,
      addRowDimensionMutate,
      deleteRowDimension,
      AddRowDimensionPosition
    }
  }
})
</script>
