<template lang="pug">
  v-menu(bottom close-on-content-click)
    template(#activator="{ on: onMenu }")
      v-tooltip(right open-delay="1000")
        template(#activator="{ on: onTooltip, attrs }")
          slot(:onMenu="onMenu" :onTooltip="onTooltip" :attrs="attrs")
        span {{ t('dcis.grid.rowControl.updatedAt', { updatedAt: dateTimeHM(buildRow.rowDimension.updatedAt) } ) }}
    v-list(dense)
      grid-row-settings(:build-row="buildRow" @close="settingsActive = false" :get-row-height="getRowHeight")
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-cog
            v-list-item-content {{ t('dcis.grid.rowControl.properties') }}
      v-list-item(@click="addRowDimension(buildRow, AddRowDimensionPosition.BEFORE)")
        v-list-item-icon
          v-icon mdi-table-row-plus-before
        v-list-item-content {{ t('dcis.grid.rowControl.addRowAbove') }}
      v-list-item(@click="addRowDimension(buildRow, AddRowDimensionPosition.AFTER)")
        v-list-item-icon
          v-icon mdi-table-row-plus-after
        v-list-item-content {{ t('dcis.grid.rowControl.addRowBelow') }}
      v-list-item(
        v-if="buildRow.rowDimension.dynamic"
        @click="addRowDimension(buildRow, AddRowDimensionPosition.INSIDE)"
      )
        v-list-item-icon
          v-icon mdi-table-row-plus-after
        v-list-item-content {{ t('dcis.grid.rowControl.addChildRow') }}
      v-list-item(@click="deleteRowDimension(+buildRow.rowDimension.id)")
        v-list-item-icon
          v-icon(color="error") mdi-table-row-remove
        v-list-item-content(color="error") {{ t('dcis.grid.rowControl.deleteRow') }}
</template>

<script lang="ts">
import { PropType, Ref } from '#app'
import { UpdateType } from '~/composables/query-common'
import { AddRowDimensionPosition } from '~/composables/grid-mutation'
import { DocumentType, SheetType, SheetQuery } from '~/types/graphql'
import { BuildRowType } from '~/types/grid'
import GridRowSettings from '~/components/dcis/grid/settings/GridRowSettings.vue'

export default defineComponent({
  components: { GridRowSettings },
  props: {
    buildRow: { type: Object as PropType<BuildRowType>, required: true },
    getRowHeight: { type: Function as PropType<(buildRow: BuildRowType) => number>, required: true }
  },
  setup () {
    const { t } = useI18n()

    const settingsActive = ref<boolean>(false)

    const { dateTimeHM } = useFilters()

    const activeDocument = inject<Ref<DocumentType>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<UpdateType<SheetQuery>>('updateActiveSheet')

    const addRowDimension = useAddRowDimensionMutation(
      computed(() => activeSheet.value.id),
      computed(() => activeDocument.value.id),
      updateSheet
    )

    const deleteRowDimension = (rowId: number) => {
      console.log('deleteRowDimension', rowId)
    }

    return {
      AddRowDimensionPosition,
      t,
      settingsActive,
      dateTimeHM,
      addRowDimension,
      deleteRowDimension
    }
  }
})
</script>
