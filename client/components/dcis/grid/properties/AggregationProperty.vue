<template lang="pug">
  v-dialog(v-model="active" v-show="!gridChoice.active.value" width="600")
    template(#activator="{ on, attrs }")
      .v-btn-toggle.mx-1(:class="themeClass" style="border-radius: 4px")
        v-btn(
          v-on="on"
          v-bind="attrs"
          :disabled="disabled || !cell"
          :class="{ 'v-btn--active': cell && cell.aggregation }"
          height="40"
        )
          v-icon mdi-sigma
    v-card
      v-card-title {{ $t('dcis.grid.sheetToolbar.aggregation.title') }}
        v-spacer
        v-btn(@click="cancel" icon)
          v-icon mdi-close
      v-card-text
        v-row(align="center")
          v-col
            v-combobox(
              v-model="aggregationKind"
              :items="aggregationItems"
              :label="$t('dcis.grid.sheetToolbar.aggregation.choice')"
            )
          v-col.text-right(v-if="aggregationKind && aggregationKind.value")
            v-btn(@click="startChoice" color="primary") {{ $t('dcis.grid.sheetToolbar.aggregation.addCells') }}
        v-list(v-if="!fromCellsLoading")
          v-list-item(v-for="fromCell in fromCells" :key="fromCell.id")
            v-list-item-content
              v-list-item-title {{ cellPosition(fromCell) }}
              v-list-item-subtitle
                | {{ $t('dcis.grid.sheetToolbar.aggregation.defaultValue', { value: fromCell.default }) }}
            v-list-item-action
              v-btn(@click="deleteMutate({ cellId: cell.id, targetCellId: fromCell.id })" icon)
                v-icon(color="error") mdi-close
        v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, onUnmounted, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import {
  AddValuesCellsMutation,
  AddValuesCellsMutationVariables,
  CellType, DeleteValueCellMutation, DeleteValueCellMutationVariables,
  ValueCellsQuery,
  ValueCellsQueryVariables
} from '~/types/graphql'
import { useCommonQuery, useI18n } from '~/composables'
import { positionToLetter } from '~/services/grid'
import valueCellsQuery from '~/gql/dcis/queries/value_cells.graphql'
import addValuesCellsMutation from '~/gql/dcis/mutations/cell/add_values_cells.graphql'
import deleteValuesCellMutation from '~/gql/dcis/mutations/cell/delete_values_cell.graphql'
import { END_CHOICE_EVENT, EndChoiceEventType, GridChoiceType } from '~/composables/grid-choice'

const aggregationKinds = t => ([
  { text: t('dcis.grid.sheetToolbar.aggregation.kinds.empty'), value: null },
  ...['sum', 'avg', 'max', 'min'].map(value => ({
    text: t(`dcis.grid.sheetToolbar.aggregation.kinds.${value}`),
    value
  }))
])

export default defineComponent({
  inheritAttrs: false,
  props: {
    gridChoice: { type: Object as PropType<GridChoiceType>, required: true },
    activeSheetIndex: { type: Number, default: null },
    disabled: { type: Boolean, default: true },
    cell: { type: Object as PropType<CellType>, default: null },
    themeClass: { type: String, required: true }
  },
  emits: ['changeKind'],
  setup (props, { emit }) {
    const { t } = useI18n()
    const active = ref<boolean>(false)

    const aggregationItems = aggregationKinds(t)
    const aggregationKind = computed({
      get: () => (aggregationItems.reduce((a, c) => ({ [c.value]: c, ...a }), {})[props.cell?.aggregation]),
      set: value => emit('changeKind', value.value)
    })

    const {
      data: fromCells,
      loading: fromCellsLoading,
      addUpdate,
      deleteUpdate
    } = useCommonQuery<ValueCellsQuery, ValueCellsQueryVariables, 'valueCells'>({
      document: valueCellsQuery,
      variables: () => ({ cellId: props.cell?.id }),
      options: () => ({ enabled: Boolean(props.cell) && active.value })
    })

    const cellPosition = (fc: ValueCellsQuery['valueCells'][number]) => (
      `${fc.sheet.name}!${positionToLetter(fc.column.index)}${fc.row.index}`
    )

    const { mutate: addMutate } = useMutation<
      AddValuesCellsMutation,
      AddValuesCellsMutationVariables
    >(addValuesCellsMutation, {
      update: (cache, result) => {
        if (!result.data.addValuesCells.errors.length) {
          addUpdate(cache, result, 'cells')
        }
      }
    })
    const { mutate: deleteMutate } = useMutation<
      DeleteValueCellMutation,
      DeleteValueCellMutationVariables
    >(deleteValuesCellMutation, {
      update: deleteUpdate
    })

    const cancel = () => {
      emit('close')
      active.value = false
    }

    const startChoice = () => {
      props.gridChoice.startChoice('AggregationProperty', props.cell, props.activeSheetIndex)
      cancel()
    }

    const endChoiceEventHandler = ({ controlName, targetCell, cells }: EndChoiceEventType) => {
      if (controlName === 'AggregationProperty') {
        addMutate({ cellId: targetCell.id, cellsId: cells.map((c: CellType) => c.id) })
        active.value = true
      }
    }
    props.gridChoice.on(END_CHOICE_EVENT, endChoiceEventHandler)
    onUnmounted(() => {
      props.gridChoice.removeListener(END_CHOICE_EVENT, endChoiceEventHandler)
    })

    return {
      active,
      cancel,
      fromCells,
      fromCellsLoading,
      startChoice,
      cellPosition,
      deleteMutate,
      aggregationKind,
      aggregationItems
    }
  }
})
</script>
