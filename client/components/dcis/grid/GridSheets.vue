<template lang="pug">
div
  v-tabs(ref="tabs" :class="{ 'mb-2': mode === GridMode.WRITE }" v-model="activeSheetIndex")
    slot(name="settings")
    slot(name="tabs" :sheets="sheets" :update-size="updateSize")
      v-tab(v-if="showAttributes" key="attributes") Атрибуты
      v-tab(v-for="sheet in sheets" :key="sheet.id") {{ sheet.name }}
  grid-sheet-toolbar(
    v-if="mode === GridMode.CHANGE"
    :grid-choice="gridChoice"
    :active-sheet-index="activeSheetIndex"
    :update-active-sheet="updateActiveSheet"
    :selected-cells-options="selectedCellsOptions"
    :selected-column-dimensions-options="selectedColumnDimensionsOptions"
    :selected-row-dimensions-options="selectedRowDimensionsOptions"
  )
  grid-choice-cells(:grid-choice="gridChoice")
  v-tabs-items.grid-sheet__tabs-items(v-model="activeSheetIndex")
    slot(v-if="showAttributes" name="attributes")
    v-tab-item(v-for="sheet in sheets" :key="sheet.id")
      grid(
        v-if="activeSheet && activeSheet.id === sheet.id"
        ref="grid"
        :mode="mode"
        :active-sheet="activeSheet"
        :update-active-sheet="updateActiveSheet"
        :active-document="activeDocument"
      )
      v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { VTabs } from 'vuetify/lib/components/VTabs'
import { computed, defineComponent, onBeforeUnmount, PropType, ref } from '#app'
import {
  BaseSheetType,
  DocumentType,
  SheetType
} from '~/types/graphql'
import {
  CellsOptionsType,
  ColumnDimensionsOptionsType,
  GridMode,
  RowDimensionsOptionsType,
  UpdateSheetType
} from '~/types/grid'
import GridSheetToolbar from '~/components/dcis/grid/GridSheetToolbar.vue'
import Grid from '~/components/dcis/grid/Grid.vue'
import GridChoiceCells from '~/components/dcis/grid/GridChoiceCells.vue'
import { CANCEL_EVENT, CancelEventType, END_CHOICE_EVENT, useGridChoice } from '~/composables/grid-choice'

export default defineComponent({
  components: { GridChoiceCells, GridSheetToolbar, Grid },
  props: {
    value: { type: Number, required: true },
    mode: { type: Number, required: true },
    sheets: { type: Array as PropType<BaseSheetType[]>, required: true },
    activeSheet: { type: Object as PropType<SheetType>, default: null },
    updateActiveSheet: { type: Function as PropType<UpdateSheetType>, required: true },
    activeDocument: { type: Object as PropType<DocumentType>, default: null },
    showAttributes: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const tabs = ref<InstanceType<typeof VTabs> | null>(null)
    const grid = ref<InstanceType<typeof Grid>[] | null>(null)

    const activeSheetIndex = computed<number>({
      get () {
        return props.value
      },
      set (value: number) {
        emit('input', value)
      }
    })

    const selectedCellsOptions = computed<CellsOptionsType | null>(() =>
      grid.value && grid.value.length ? grid.value[0].selectedCellsOptions : null
    )
    const selectedColumnDimensionsOptions = computed<ColumnDimensionsOptionsType | null>(() =>
      grid.value && grid.value.length ? grid.value[0].selectedColumnDimensionsOptions : null
    )
    const selectedRowDimensionsOptions = computed<RowDimensionsOptionsType | null>(() =>
      grid.value && grid.value.length ? grid.value[0].selectedRowDimensionsOptions : null
    )

    const updateSize = () => {
      tabs.value.onResize()
    }

    const gridChoice = useGridChoice(props.mode, computed(() => props.activeSheet), selectedCellsOptions)
    if (props.mode === GridMode.CHANGE) {
      const cancelEventHandler = ({ targetCell, sheetIndex }: CancelEventType) => {
        activeSheetIndex.value = sheetIndex
        setTimeout(() => {
          grid.value && grid.value.length && grid.value[0].selectSelectionCell(targetCell)
        }, 0)
      }
      gridChoice.on(END_CHOICE_EVENT, cancelEventHandler)
      gridChoice.on(CANCEL_EVENT, cancelEventHandler)
      onBeforeUnmount(() => {
        gridChoice.removeListener(END_CHOICE_EVENT, cancelEventHandler)
        gridChoice.removeListener(CANCEL_EVENT, cancelEventHandler)
      })
    }

    return {
      GridMode,
      tabs,
      grid,
      activeSheetIndex,
      selectedCellsOptions,
      selectedColumnDimensionsOptions,
      selectedRowDimensionsOptions,
      updateSize,
      gridChoice
    }
  }
})
</script>

<style lang="sass">
.grid-sheet__tabs-items
  height: calc(100vh - 285px)
  overflow: visible !important
</style>
