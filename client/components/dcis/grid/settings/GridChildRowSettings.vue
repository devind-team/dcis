<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.grid.childRowSettings.header'))"
  :subheader="String($t('dcis.grid.childRowSettings.subheader', { updatedAt: dateTimeHM(row.updatedAt) }))"
  :mutation="changeChildRowDimensionHeightMutation"
  :variables="variables"
  :optimistic-response="optimisticResponse"
  :update="update"
  :button-text="String($t('dcis.grid.childRowSettings.buttonText'))"
  i18n-path="dcis.grid.childRowSettings"
  mutation-name="changeChildRowDimensionHeight"
  @close="$emit('close')"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.grid.childRowSettings.height'))"
      rules="required|integer|min_value:0"
    )
      v-text-field(
        v-model="height"
        :error-messages="errors"
        :success="valid"
        :label="$t('dcis.grid.childRowSettings.height')"
      )
</template>

<script lang="ts">
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { computed, inject, defineComponent, PropType } from '#app'
import { useFilters, UpdateType } from '~/composables'
import { UpdateActiveSheetInject } from '~/types/grid'
import {
  RowDimensionType,
  DocumentSheetQuery,
  ChangeChildRowDimensionHeightMutation,
  ChangeChildRowDimensionHeightMutationVariables
} from '~/types/graphql'
import { updateChildRowDimension } from '~/composables/grid-mutations'
import changeChildRowDimensionHeightMutation from '~/gql/dcis/mutations/document/change_child_row_dimension_height.graphql'
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

    const variables = computed<ChangeChildRowDimensionHeightMutationVariables>(() => ({
      rowDimensionId: props.row.id,
      height: Number(height.value)
    }))
    const optimisticResponse = computed<ChangeChildRowDimensionHeightMutation>(() => ({
      __typename: 'Mutation',
      changeChildRowDimensionHeight: {
        __typename: 'ChangeChildRowDimensionHeightMutationPayload',
        success: true,
        errors: [],
        rowDimensionId: props.row.id,
        height: Number(height.value),
        updatedAt: new Date().toISOString()
      }
    }))

    const updateSheet = inject(UpdateActiveSheetInject)
    const update = (
      dataProxy: DataProxy,
      result: Omit<FetchResult<ChangeChildRowDimensionHeightMutation>, 'context'>
    ) => {
      updateChildRowDimension(updateSheet.value as UpdateType<DocumentSheetQuery>, dataProxy, result)
    }

    return { changeChildRowDimensionHeightMutation, dateTimeHM, height, variables, optimisticResponse, update }
  }
})
</script>
