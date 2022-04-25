<template lang="pug">
  v-row
    v-col
      v-btn-toggle.ml-1(v-model="formatting" multiple dense)
        v-btn(value="strong" :disabled="!selectionCells.length") #[v-icon mdi-format-bold]
        v-btn(value="italic" :disabled="!selectionCells.length") #[v-icon mdi-format-italic]
        // v-btn(value="underline" :disabled="!selectionCells.length") #[v-icon mdi-format-underline]
      v-btn-toggle.mx-1(v-model="horizontalAlignValue" dense)
        v-btn(:disabled="!selectionCells.length" value="left") #[v-icon mdi-format-align-left]
        v-btn(:disabled="!selectionCells.length" value="center") #[v-icon mdi-format-align-center]
        v-btn(:disabled="!selectionCells.length" value="right" ) #[v-icon mdi-format-align-right]
      v-btn-toggle.mx-1(v-model="verticalAlignValue" dense)
        v-btn(:disabled="!selectionCells.length" value="top") #[v-icon mdi-format-align-top]
        v-btn(:disabled="!selectionCells.length" value="middle") #[v-icon mdi-format-align-middle]
        v-btn(:disabled="!selectionCells.length" value="bottom" ) #[v-icon mdi-format-align-bottom]
      v-btn-toggle
        v-combobox.mx-1(v-model="sizeValue" :items="sizes" :disabled="!selectionCells.length" label="Шрифт" style="width: 150px" dense)
        v-combobox.mx-1(v-model="kindValue" :items="kinds" :disabled="!selectionCells.length" label="Тип" style="width: 150px"  dense)
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import type { ComputedRef, PropType, WritableComputedRef } from '#app'
import { computed, defineComponent } from '#app'
import { useI18n } from '~/composables'
import { cellKinds } from '~/composables/grid'
import { BuildCellType, CellOptionsType } from '~/types/grid-types'
import {
  CellType,
  ChangeCellsOptionMutation,
  ChangeCellsOptionMutationPayload,
  ChangeCellsOptionMutationVariables
} from '~/types/graphql'
import changeCellsOption from '~/gql/dcis/mutations/sheet/change_cells_option.graphql'

export type ChangeCellOptionMutationResultType = { data: { changeCellsOption: ChangeCellsOptionMutationPayload } }
type DocumentUpdateType = (cache: any, result: any, transform: (dc: any, result: any) => any) => any

export default defineComponent({
  props: {
    sheetId: { type: String, required: true },
    selectionCells: { type: Array as PropType<BuildCellType[]>, required: true },
    selectionCellsOptions: { type: Object as PropType<CellOptionsType>, required: true },
    update: { type: Function as PropType<DocumentUpdateType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { mutate } = useMutation<ChangeCellsOptionMutation, ChangeCellsOptionMutationVariables>(changeCellsOption, {
      update: (cache: DataProxy | any, result: ChangeCellOptionMutationResultType | any) => props.update(
        cache,
        result,
        (dataCache, { data: { changeCellsOption: { success, cells } } }: ChangeCellOptionMutationResultType) => {
          if (success) {
            const cellsId: string[] = cells.map((cell: CellType) => (cell.id))
            const sheetCells: CellType[] = dataCache.document.sheets
              .find(sheet => sheet.id === props.sheetId)
              .cells.filter(c => !cellsId.includes(c.id))
            sheetCells.push(...cells)
            dataCache.document.sheets.find(sheet => sheet.id === props.sheetId).cells = sheetCells
          }
          return dataCache
        }
      )
    })
    const cellsId: ComputedRef<number[]> = computed<number[]>(() => props.selectionCells.map(e => parseInt(e.cell.id)))

    const kinds: ComputedRef<{ text: string, value: string }[]> = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.cellKinds.${k}`) as string, value: k })))
    )
    const kindValue: WritableComputedRef<any> = computed({
      get: () => (kinds.value.find(k => (k.value === props.selectionCellsOptions.kind))),
      set: value => mutate({ cellsId: cellsId.value, field: 'kind', value: value.value })
    })

    const sizes: { text: string, value: number }[] = Array
      .from(new Array(19).keys())
      .map((e: number) => e + 6)
      .map((e: number) => ({ text: `${e}px`, value: e }))
    const sizeValue: WritableComputedRef<{ text: string, value: number }> = computed<{ text: string, value: number }>({
      get: () => (sizes.find(s => (s.value === props.selectionCellsOptions.size))),
      set: value => mutate({ cellsId: cellsId.value, field: 'size', value: String(value.value) })
    })

    const formatting: WritableComputedRef<string[]> = computed<string[]>({
      get: () => (['strong', 'italic', 'underline'].filter(f => props.selectionCellsOptions[f])),
      set: (value) => {
        const diff: string[] = formatting.value.length > value.length
          ? formatting.value.filter(e => !value.includes(e))
          : value.filter(v => !formatting.value.includes(v))
        if (diff.length) {
          let field: string | null = null
          const [intersectionFormat, intersectionValue] = formatting.value.length > value.length
            ? [formatting.value, value]
            : [value, formatting.value]
          for (const v of intersectionFormat) {
            if (!intersectionValue.includes(v)) {
              field = v
              break
            }
          }
          const val: string = String(!props.selectionCellsOptions[field])
          mutate({ cellsId: cellsId.value, field, value: val })
        }
      }
    })

    const horizontalAlignValue: WritableComputedRef<string | null> = computed<string | null>({
      get: () => (props.selectionCellsOptions.horizontalAlign),
      set: value => mutate({ cellsId: cellsId.value, field: 'horizontal_align', value })
    })
    const verticalAlignValue: WritableComputedRef<string | null> = computed<string | null>({
      get: () => (props.selectionCellsOptions.verticalAlign),
      set: value => mutate({ cellsId: cellsId.value, field: 'vertical_align', value })
    })

    return {
      cellsId,
      formatting,
      kinds,
      kindValue,
      sizes,
      horizontalAlignValue,
      verticalAlignValue,
      sizeValue
    }
  }
})
</script>
