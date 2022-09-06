<template lang="pug">
div
  v-tabs(ref="tabs" :class="{ 'mb-2': mode === GridMode.WRITE }" v-model="activeSheetIndex")
    slot(name="settings")
    slot(name="tabs" :sheets="sheets" :update-size="updateSize")
      v-tab(v-for="sheet in sheets" :key="sheet.id") {{ sheet.name }}
  grid-sheet-toolbar(
    v-if="mode === GridMode.CHANGE"
    :update-active-sheet="updateActiveSheet"
    :selected-cells-options="selectedCellsOptions"
    :selected-column-dimensions-options="selectedColumnDimensionsOptions"
    :selected-row-dimensions-options="selectedRowDimensionsOptions"
  )
  v-tabs-items.grid-sheet__tabs-items(v-model="activeSheetIndex")
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
import { computed, defineComponent, PropType, ref } from '#app'
import { BaseSheetType, DocumentType, SheetType } from '~/types/graphql'
import {
  CellsOptionsType,
  ColumnDimensionsOptionsType,
  GridMode,
  RowDimensionsOptionsType,
  UpdateSheetType
} from '~/types/grid'
import GridSheetToolbar from '~/components/dcis/grid/GridSheetToolbar.vue'
import Grid from '~/components/dcis/grid/Grid.vue'

export default defineComponent({
  components: { GridSheetToolbar, Grid },
  props: {
    value: { type: Number, required: true },
    mode: { type: Number, required: true },
    sheets: { type: Array as PropType<BaseSheetType[]>, required: true },
    activeSheet: { type: Object as PropType<SheetType>, default: null },
    updateActiveSheet: { type: Function as PropType<UpdateSheetType>, required: true },
    activeDocument: { type: Object as PropType<DocumentType>, default: null }
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

    return {
      GridMode,
      tabs,
      grid,
      activeSheetIndex,
      selectedCellsOptions,
      selectedColumnDimensionsOptions,
      selectedRowDimensionsOptions,
      updateSize
    }
  }
})
</script>

<style lang="sass">
.grid-sheet__tabs-items
  height: calc(100vh - 337px)
  overflow: visible !important
</style>
