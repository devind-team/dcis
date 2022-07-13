<template lang="pug">
v-menu(v-model="active" bottom close-on-content-click)
  template(#activator="{ on, attrs }")
    slot(:on="on" :attrs="attrs")
  v-list(dense)
    grid-row-settings(:row="row" @close="active = false" :get-row-height="getRowHeight")
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
import { DocumentType, SheetType, RowDimensionType, DocumentSheetQuery } from '~/types/graphql'
import { UpdateType } from '~/composables/query-common'
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

    const activeDocument = inject<Ref<DocumentType | null>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateType<DocumentSheetQuery>>>('updateActiveSheet')

    const addRowDimensionMutate = useAddRowDimensionMutation(
      computed(() => activeDocument.value ? activeDocument.value.id : null),
      activeSheet,
      updateSheet
    )

    const deleteRowDimensionMutate = useDeleteRowDimensionMutation(activeSheet, updateSheet)

    const deleteRowDimension = async (row: RowDimensionType) => {
      await deleteRowDimensionMutate(row)
      props.clearSelection()
    }

    return {
      t,
      active,
      addRowDimensionMutate,
      deleteRowDimension,
      AddRowDimensionPosition
    }
  }
})
</script>
