<template lang="pug">
  v-dialog(v-model="active" width="600")
    template(#activator="{ on, attrs }")
      div(class="mr-1 v-item-group theme--light v-btn-toggle")
        v-btn(
          v-on="on"
          v-bind="attrs"
          :disabled="disabled || !cell"
          :class="[{ 'v-btn--active': cell && cell.aggregation }, themeClass]"
          class="v-btn--has-bg theme--light v-size--default"
          width="40"
          height="40"
        )
          v-icon mdi-sigma
    v-card
      v-card-title {{ t('dcis.grid.sheetToolbar.aggregationTitle') }}
        v-spacer
        v-btn(@click="cancel" icon)
          v-icon mdi-close
      v-card-text
        v-combobox(v-model="aggregationKind" :items="aggregationItems" :label="t('dcis.grid.sheetToolbar.aggregationChoice')")
        v-list(v-if="!fromCellsLoading")
          v-list-item(v-for="fromCell in fromCells" :key="fromCell.id")
            v-list-item-content
              v-list-item-title {{ cellPosition(fromCell) }}
              v-list-item-subtitle {{ t('dcis.grid.sheetToolbar.aggregationDefault', { value: fromCell.default }) }}
            v-list-item-action
              v-btn(@click="deleteMutate({ cellId: cell.id, targetCellId: fromCell.id })" icon)
                v-icon(color="error") mdi-close
        v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import {
  CellType, DeleteValueCellMutation, DeleteValueCellMutationVariables,
  ValueCellsQuery,
  ValueCellsQueryVariables
} from '~/types/graphql'
import { useCommonQuery, useI18n } from '~/composables'
import { positionToLetter } from '~/services/grid'
import valueCellsQuery from '~/gql/dcis/queries/value_cells.graphql'
import deleteValuesCellMutation from '~/gql/dcis/mutations/cell/delete_values_cell.graphql'

const aggregationKinds = t => ([
  { text: t('dcis.grid.sheetToolbar.aggregationKind.empty'), value: null },
  ...['sum', 'avg', 'max', 'min'].map(value => ({
    text: t(`dcis.grid.sheetToolbar.aggregationKind.${value}`),
    value
  }))
])

export default defineComponent({
  inheritAttrs: false,
  props: {
    disabled: { type: Boolean, default: true },
    cell: { type: Object as PropType<CellType>, default: null },
    themeClass: { type: String, default: 'theme--light' }
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
      deleteUpdate
    } = useCommonQuery<ValueCellsQuery, ValueCellsQueryVariables, 'valueCells'>({
      document: valueCellsQuery,
      variables: () => ({ cellId: props.cell?.id }),
      options: () => ({ enabled: Boolean(props.cell) })
    })

    const cellPosition = (fc: ValueCellsQuery['valueCells'][number]) => (`${fc.sheet.name}!${positionToLetter(fc.column.index)}${fc.row.index}`)

    const { mutate: deleteMutate } = useMutation<DeleteValueCellMutation, DeleteValueCellMutationVariables>(deleteValuesCellMutation, {
      update: deleteUpdate
    })

    const cancel = () => {
      emit('close')
      active.value = false
    }

    return {
      active,
      cancel,
      fromCells,
      fromCellsLoading,
      cellPosition,
      deleteMutate,
      aggregationKind,
      aggregationItems,
      t
    }
  }
})
</script>
