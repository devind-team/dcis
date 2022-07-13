<template lang="pug">
v-row
  v-col.my-2.d-flex.align-center
    v-btn-toggle(v-model="formatting" multiple)
      v-btn(:disabled="disabled" value="strong" height="40")
        v-icon mdi-format-bold
      v-btn(:disabled="disabled" value="italic" height="40")
        v-icon mdi-format-italic
      v-btn(:disabled="disabled" value="underline" height="40")
        v-icon mdi-format-underline
      v-btn(:disabled="disabled" value="strike" height="40")
        v-icon mdi-format-strikethrough
    v-btn-toggle.mx-1(v-model="horizontalAlign")
      v-btn(:disabled="disabled" value="left" height="40")
        v-icon mdi-format-align-left
      v-btn(:disabled="disabled" value="center" height="40")
        v-icon mdi-format-align-center
      v-btn(:disabled="disabled" value="right" height="40")
        v-icon mdi-format-align-right
    v-btn-toggle.mx-1(v-model="verticalAlign")
      v-btn(:disabled="disabled" value="top" height="40")
        v-icon mdi-format-align-top
      v-btn(:disabled="disabled" value="middle" height="40")
        v-icon mdi-format-align-middle
      v-btn(:disabled="disabled" value="bottom" height="40")
        v-icon mdi-format-align-bottom
    v-combobox.mx-1.shrink(
      v-model="size"
      :label="t('dcis.grid.sheetToolbar.fontSize')"
      :items="sizes"
      :disabled="disabled"
      style="width: 170px"
      filled
      outlined
      hide-details
      dense
    )
    v-combobox.ml-1.shrink(
      v-model="kind"
      :label="t('dcis.grid.sheetToolbar.kind')"
      :items="kinds"
      :disabled="disabled"
      style="width: 170px"
      filled
      outlined
      hide-details
      dense
    )
</template>

<script lang="ts">
import { PropType, Ref } from '#app'
import { UpdateType } from '~/composables'
import { DocumentType, DocumentSheetQuery, SheetType } from '~/types/graphql'
import { CellsOptionsType } from '~/types/grid'

export default defineComponent({
  props: {
    selectedCellsOptions: { type: Object as PropType<CellsOptionsType>, default: null }
  },
  setup (props) {
    const { t } = useI18n()

    const activeDocument = inject<Ref<DocumentType | null>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateType<DocumentSheetQuery>>>('updateActiveSheet')
    const changeCellsOption = useChangeCellsOptionMutation(
      computed(() => activeDocument.value ? activeDocument.value.id : ''),
      computed(() => activeSheet.value.id),
      updateSheet
    )

    const disabled = computed<boolean>(() => !props.selectedCellsOptions)

    const formatting = computed<string[]>({
      get: () => !disabled.value
        ? (['strong', 'italic', 'underline', 'strike'].filter(f => !!props.selectedCellsOptions[f]))
        : [],
      set: (value) => {
        const diff = formatting.value.length > value.length
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
          let val: string | null = null
          if (field === 'underline') {
            val = props.selectedCellsOptions.underline ? null : 'single'
          } else {
            val = String(!props.selectedCellsOptions[field])
          }
          changeCellsOption(props.selectedCellsOptions.cells, field, val)
        }
      }
    })

    const horizontalAlign = computed<string | null>({
      get: () => !disabled.value ? props.selectedCellsOptions.horizontalAlign : null,
      set: value => changeCellsOption(props.selectedCellsOptions.cells, 'horizontalAlign', value)
    })

    const verticalAlign = computed<string | null>({
      get: () => !disabled.value ? props.selectedCellsOptions.verticalAlign : null,
      set: value => changeCellsOption(props.selectedCellsOptions.cells, 'verticalAlign', value)
    })

    const sizes = Array
      .from(new Array(19).keys())
      .map((e: number) => e + 6)
      .map((e: number) => ({ text: `${e}px`, value: e }))
    const size = computed<{text: string, value: number} | null>({
      get: () => !disabled.value ? sizes.find(s => s.value === props.selectedCellsOptions.size) : null,
      set: value => changeCellsOption(props.selectedCellsOptions.cells, 'size', String(value.value))
    })

    const kinds = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.grid.cellKinds.${k}`) as string, value: k })))
    )
    const kind = computed<{ text: string, value: string } | null>({
      get: () => !disabled.value ? kinds.value.find(k => k.value === props.selectedCellsOptions.kind) : null,
      set: value => changeCellsOption(props.selectedCellsOptions.cells, 'kind', value.value)
    })

    return {
      t,
      disabled,
      formatting,
      horizontalAlign,
      verticalAlign,
      sizes,
      size,
      kinds,
      kind
    }
  }
})
</script>
