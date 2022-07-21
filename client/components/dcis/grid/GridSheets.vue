<template lang="pug">
div
  v-tabs(v-model="activeSheetIndex")
    slot(name="settings")
    v-tab(v-for="sheet in sheets" :key="sheet.id") {{ sheet.name }}
  grid-sheet-toolbar(:selected-cells-options="selectedCellsOptions")
  v-tabs-items(v-model="activeSheetIndex" style="height: calc(100vh - 337px)")
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
import { PropType, provide, toRef } from '#app'
import { DocumentType, BaseSheetType, SheetType } from '~/types/graphql'
import { UpdateSheetType, CellsOptionsType } from '~/types/grid'
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
    const grid = ref<InstanceType<typeof Grid>[] | null>(null)

    const activeSheetIndex = computed<number>({
      get () {
        return props.value
      },
      set (value: number) {
        emit('input', value)
      }
    })

    const activeSheet = toRef(props, 'activeSheet')
    const updateActiveSheet = toRef(props, 'updateActiveSheet')
    const activeDocument = toRef(props, 'activeDocument')

    provide('mode', props.mode)
    provide('activeSheet', activeSheet)
    provide('updateActiveSheet', updateActiveSheet)
    provide('activeDocument', activeDocument)

    const selectedCellsOptions = computed<CellsOptionsType | null>(() =>
      grid.value && grid.value.length ? grid.value[0].selectedCellsOptions : null
    )

    return { grid, activeSheetIndex, selectedCellsOptions }
  }
})
</script>
