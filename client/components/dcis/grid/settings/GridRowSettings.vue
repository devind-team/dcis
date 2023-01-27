<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.grid.rowSettings.header'))"
  :subheader="String($t('dcis.grid.rowSettings.subheader', { updatedAt: dateTimeHM(row.updatedAt) }))"
  :mutation="changeRowDimensionMutation"
  :variables="variables"
  :optimistic-response="optimisticResponse"
  :update="update"
  :button-text="String($t('dcis.grid.rowSettings.buttonText'))"
  i18n-path="dcis.grid.rowSettings"
  mutation-name="changeRowDimension"
  @close="$emit('close')"
  @click:outside="$emit('close')"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.grid.rowSettings.height'))"
      rules="required|integer|min_value:0"
    )
      v-text-field(
        v-model="height"
        :error-messages="errors"
        :success="valid"
        :label="$t('dcis.grid.rowSettings.height')"
      )
    v-checkbox(v-model="hidden" :label="$t('dcis.grid.rowSettings.hide')" color="primary")
    v-checkbox(
      v-model="dynamic"
      :label="$t('dcis.grid.rowSettings.makeDynamic')"
      :disabled="!!row.children.length || row.cells.some(cell => cell.rowspan !== 1)"
      color="primary"
    )
</template>

<script lang="ts">
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { ref, inject, PropType } from '#app'
import { useFilters, UpdateType } from '~/composables'
import { updateRowDimension } from '~/composables/grid-mutations'
import { UpdateActiveSheetInject } from '~/types/grid'
import {
  PeriodSheetQuery,
  RowDimensionType,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables
} from '~/types/graphql'
import changeRowDimensionMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()

    const height = ref<string>(String(props.getRowHeight(props.row)))
    const hidden = ref<boolean>(props.row.hidden)
    const dynamic = ref<boolean>(props.row.dynamic)
    watch(computed<number>(() => props.getRowHeight(props.row)), (newValue: number) => {
      height.value = String(newValue)
    })

    const variables = computed<ChangeRowDimensionMutationVariables>(() => ({
      rowDimensionId: props.row.id,
      height: Number(height.value),
      hidden: hidden.value,
      dynamic: dynamic.value
    }))
    const optimisticResponse = computed<ChangeRowDimensionMutation>(() => ({
      __typename: 'Mutation',
      changeRowDimension: {
        __typename: 'ChangeRowDimensionMutationPayload',
        success: true,
        errors: [],
        rowDimension: {
          ...variables.value,
          id: props.row.id,
          updatedAt: new Date().toISOString(),
          __typename: 'ChangeRowDimensionType'
        }
      }
    }))

    const updateSheet = inject(UpdateActiveSheetInject)
    const update = (dataProxy: DataProxy, result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>) => {
      updateRowDimension(updateSheet.value as UpdateType<PeriodSheetQuery>, dataProxy, result)
    }

    return {
      changeRowDimensionMutation,
      dateTimeHM,
      height,
      hidden,
      dynamic,
      variables,
      optimisticResponse,
      update
    }
  }
})
</script>
