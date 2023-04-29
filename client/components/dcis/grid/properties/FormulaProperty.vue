<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.grid.sheetToolbar.formula.header'))"
  :button-text="String($t('dcis.grid.sheetToolbar.formula.buttonText'))"
  :mutation="changeCellFormulaMutation"
  :variables="variables"
  :update="update"
  mutation-name="changeCellFormula"
  i18n-path="dcis.grid.sheetToolbar.formula"
  @close="close"
)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    v-text-field(
      v-model="formula"
      :label="$t('dcis.grid.sheetToolbar.formula.formula')"
      clearable
    )
    v-checkbox(v-model="recalculate", :label="$t('dcis.grid.sheetToolbar.formula.recalculate')")
</template>

<script lang="ts">
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { defineComponent, PropType, ref, watch, computed } from '#app'
import {
  SheetType,
  CellType,
  ChangeCellFormulaMutation,
  ChangeCellFormulaMutationVariables,
  PeriodSheetQuery
} from '~/types/graphql'
import { findCell } from '~/services/grid'
import { UpdateType } from '~/composables'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import changeCellFormulaMutation from '~/gql/dcis/mutations/cell/change_cell_formula.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    cell: { type: Object as PropType<CellType>, default: null },
    updateActiveSheet: { type: Function as PropType<UpdateType<PeriodSheetQuery>>, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)

    const formula = ref<string>('')
    watch(() => props.cell, (newValue) => {
      formula.value = newValue ? newValue.formula : ''
    })
    const recalculate = ref<boolean>(true)

    const variables = computed<ChangeCellFormulaMutationVariables>(() => ({
      cellId: props.cell ? props.cell.id : '',
      formula: formula.value,
      recalculate: recalculate.value
    }))

    const update = (dataProxy: DataProxy, result: Omit<FetchResult<ChangeCellFormulaMutation>, 'context'>) => {
      if (result.data.changeCellFormula.success) {
        props.updateActiveSheet(dataProxy, result, (
          data: PeriodSheetQuery, {
            data: { changeCellFormula }
          }: Omit<FetchResult<ChangeCellFormulaMutation>, 'context'>
        ) => {
          const cell = findCell(
            data.periodSheet as SheetType,
            (c: CellType) => c.id === changeCellFormula.cellId
          )
          cell.formula = changeCellFormula.formula
          return data
        })
      }
    }

    const close = () => {
      emit('close')
      active.value = false
      formula.value = props.cell ? props.cell.formula : ''
      recalculate.value = true
    }

    return { changeCellFormulaMutation, active, formula, recalculate, variables, update, close }
  }
})
</script>
