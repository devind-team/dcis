<template lang="pug">
v-row
  v-col.my-2.d-flex.align-center
    v-btn-toggle.mr-1(v-model="formatting" multiple)
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
    v-tooltip(bottom)
      template(#activator="{ on: onTooltip, attrs }")
        div(v-on="onTooltip" v-bind="attrs")
          aggregation-property(
            @changeKind="aggregationCell ? changeCellsOption([aggregationCell], 'aggregation', $event) : null"
            :grid-choice="gridChoice"
            :active-sheet-index="activeSheetIndex"
            :cell="aggregationCell"
            :disabled="disabled"
            :themeClass="themeClass"
          )
      span {{ $t('dcis.grid.sheetToolbar.aggregation') }}
    v-tooltip(bottom)
      template(#activator="{ on, attrs }")
        div(v-on="on" v-bind="attrs")
          v-btn-toggle.mx-1(v-model="properties" multiple)
            v-btn(:disabled="disabled" value="readonly" height="40")
              v-icon mdi-pencil-off
      span {{ $t('dcis.grid.sheetToolbar.readonly') }}
    v-tooltip(bottom)
      template(#activator="{ on, attrs }")
        div(v-on="on" v-bind="attrs")
          v-btn-toggle.mx-1(v-model="dimensionsProperties" multiple)
            v-btn(:disabled="fixedDisabled" value="fixed" height="40")
              v-icon mdi-table-lock
      span {{ $t('dcis.grid.sheetToolbar.fix') }}
    v-combobox.mx-1.shrink(
      v-model="size"
      :label="$t('dcis.grid.sheetToolbar.fontSize')"
      :items="sizes"
      :disabled="disabled"
      style="width: 170px"
      filled
      outlined
      hide-details
      dense
    )
    v-combobox.mx-1.shrink(
      v-model="kind"
      :label="$t('dcis.grid.sheetToolbar.kind')"
      :items="kinds"
      :disabled="disabled"
      style="width: 170px"
      filled
      outlined
      hide-details
      dense
    )
    v-tooltip(bottom)
      template(#activator="{ on, attrs }")
        div(v-on="on" v-bind="attrs")
          .v-btn-toggle.ml-1(:class="themeClass" style="border-radius: 4px 0 0 4px")
            v-btn(:disabled="commaDecreaseDisabled" height="40" @click="commaDecrease")
              v-icon mdi-decimal-comma-decrease
      span {{ $t('dcis.grid.sheetToolbar.commaDecrease') }}
    v-tooltip(bottom)
      template(#activator="{ on, attrs }")
        div(v-on="on" v-bind="attrs")
          .v-btn-toggle.mr-1(:class="themeClass" style="border-radius: 0 4px 4px 0")
            v-btn(:disabled="commaDisabled" height="40" style="border-left-width: 0" @click="commaIncrease")
              v-icon mdi-decimal-comma-increase
      span {{ $t('dcis.grid.sheetToolbar.commaIncrease') }}
</template>

<script lang="ts">
import { computed, defineComponent, inject, PropType, Ref } from '#app'
import { CellType, PeriodSheetQuery } from '~/types/graphql'
import { CellsOptionsType, ColumnDimensionsOptionsType, RowDimensionsOptionsType } from '~/types/grid'
import { useVuetify, useI18n, UpdateType } from '~/composables'
import {
  useChangeCellsOptionMutation,
  useChangeColumnDimensionsFixedMutation,
  useChangeRowDimensionsFixedMutation
} from '~/composables/grid-mutations'
import { GridChoiceType } from '~/composables/grid-choice'
import AggregationProperty from '~/components/dcis/grid/properties/AggregationProperty.vue'

export default defineComponent({
  components: { AggregationProperty },
  props: {
    gridChoice: { type: Object as PropType<GridChoiceType>, required: true },
    activeSheetIndex: { type: Number, default: null },
    selectedCellsOptions: { type: Object as PropType<CellsOptionsType>, default: null },
    selectedColumnDimensionsOptions: { type: Object as PropType<ColumnDimensionsOptionsType>, default: null },
    selectedRowDimensionsOptions: { type: Object as PropType<RowDimensionsOptionsType>, default: null }
  },
  setup (props) {
    const { t } = useI18n()
    const { isDark } = useVuetify()

    const themeClass = computed<string>(() => isDark ? 'theme--light' : 'theme--dark')

    const updateActiveSheet = inject<Ref<UpdateType<PeriodSheetQuery>>>('updateActiveSheet')
    const changeCellsOption = useChangeCellsOptionMutation(updateActiveSheet)
    const changeColumnDimensionsFixed = useChangeColumnDimensionsFixedMutation(updateActiveSheet)
    const changeRowDimensionsFixed = useChangeRowDimensionsFixedMutation(updateActiveSheet)

    const selectedDimensionsOptions = computed<ColumnDimensionsOptionsType | RowDimensionsOptionsType | null>(
      () => props.selectedColumnDimensionsOptions || props.selectedRowDimensionsOptions || null
    )

    const disabled = computed<boolean>(() => !props.selectedCellsOptions)
    const dimensionsDisabled = computed<boolean>(() => !selectedDimensionsOptions.value)
    const fixedDisabled = computed<boolean>(
      () => dimensionsDisabled.value || !selectedDimensionsOptions.value.rectangular
    )
    const commaDisabled = computed<boolean>(() =>
      disabled.value ||
      props.selectedCellsOptions.kind !== 'n' ||
      !/^(0\.0+)|(0)$/.test(props.selectedCellsOptions.numberFormat)
    )
    const commaDecreaseDisabled = computed<boolean>(
      () => commaDisabled.value || props.selectedCellsOptions.numberFormat === '0'
    )

    const formatting = computed<string[]>({
      get: () => !disabled.value
        ? ['strong', 'italic', 'underline', 'strike'].filter(f => !!props.selectedCellsOptions[f])
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
          let val: string | null
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

    const properties = computed<string[]>({
      get: () => {
        if (disabled.value) {
          return []
        }
        if (!props.selectedCellsOptions.editable) {
          return ['readonly']
        }
        return []
      },
      set: (value) => {
        const diff = properties.value.length > value.length
          ? properties.value.filter(e => !value.includes(e))
          : value.filter(v => !properties.value.includes(v))
        if (diff.length) {
          let field: string | null = null
          const [intersectionFormat, intersectionValue] = properties.value.length > value.length
            ? [properties.value, value]
            : [value, properties.value]
          for (const v of intersectionFormat) {
            if (!intersectionValue.includes(v)) {
              field = v
              break
            }
          }
          if (field === 'readonly') {
            field = 'editable'
          }
          changeCellsOption(props.selectedCellsOptions.cells, field, String(!props.selectedCellsOptions[field]))
        }
      }
    })

    const aggregationCell = computed<CellType | null>(() => (
      props.selectedCellsOptions && props.selectedCellsOptions.cells.length === 1
        ? props.selectedCellsOptions.cells[0]
        : null)
    )

    const dimensionsProperties = computed<string[]>({
      get: () => {
        if (dimensionsDisabled.value || fixedDisabled.value) {
          return []
        }
        if (selectedDimensionsOptions.value.fixed) {
          return ['fixed']
        }
        return []
      },
      set: (value) => {
        const diff = dimensionsProperties.value.length > value.length
          ? dimensionsProperties.value.filter(e => !value.includes(e))
          : value.filter(v => !dimensionsProperties.value.includes(v))
        if (diff.length) {
          let field: string | null = null
          const [intersectionFormat, intersectionValue] = dimensionsProperties.value.length > value.length
            ? [dimensionsProperties.value, value]
            : [value, dimensionsProperties.value]
          for (const v of intersectionFormat) {
            if (!intersectionValue.includes(v)) {
              field = v
              break
            }
          }
          if (field === 'fixed') {
            if (props.selectedColumnDimensionsOptions) {
              changeColumnDimensionsFixed(
                props.selectedColumnDimensionsOptions.columnDimensions,
                !props.selectedColumnDimensionsOptions.fixed
              )
            } else {
              changeRowDimensionsFixed(
                props.selectedRowDimensionsOptions.rowDimensions,
                !props.selectedRowDimensionsOptions.fixed
              )
            }
          }
        }
      }
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

    const commaDecrease = () => {
      changeCellsOption(
        props.selectedCellsOptions.cells,
        'numberFormat',
        props.selectedCellsOptions.numberFormat === '0.0'
          ? '0'
          : props.selectedCellsOptions.numberFormat.slice(0, -1)
      )
    }

    const commaIncrease = () => {
      changeCellsOption(
        props.selectedCellsOptions.cells,
        'numberFormat',
        props.selectedCellsOptions.numberFormat === '0' ? '0.0' : props.selectedCellsOptions.numberFormat + '0'
      )
    }

    return {
      themeClass,
      disabled,
      fixedDisabled,
      commaDisabled,
      commaDecreaseDisabled,
      formatting,
      horizontalAlign,
      verticalAlign,
      properties,
      aggregationCell,
      dimensionsProperties,
      sizes,
      size,
      kinds,
      kind,
      commaDecrease,
      commaIncrease,
      changeCellsOption
    }
  }
})
</script>
