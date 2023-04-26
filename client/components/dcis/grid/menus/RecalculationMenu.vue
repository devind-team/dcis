<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.recalculationMenu.buttonText') }}
  v-list(dense width="200")
    v-list-item(@click="recalculateAllCells({ periodId: period.id })")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.recalculationMenu.recalculateAll') }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { defineComponent, PropType } from '#app'
import { PeriodType, RecalculateAllCellsMutation, RecalculateAllCellsMutationVariables } from '~/types/graphql'
import recalculateAllCellsMutation from '~/gql/dcis/mutations/values/recalculate_all_cells.graphql'

export default defineComponent({
  props: {
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup () {
    const { mutate: recalculateAllCells } = useMutation<
      RecalculateAllCellsMutation,
      RecalculateAllCellsMutationVariables
    >(recalculateAllCellsMutation)

    return { recalculateAllCells }
  }
})
</script>
