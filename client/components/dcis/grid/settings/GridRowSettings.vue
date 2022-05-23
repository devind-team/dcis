<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.rowSettings.header'))"
    :subheader="String(t('dcis.grid.rowSettings.subheader', { updatedAt: dateTimeHM(row.updatedAt) }))"
    :mutation="changeRowMutation"
    :variables="variables"
    :optimistic-response="optimisticResponse"
    :update="update"
    :button-text="String(t('dcis.grid.rowSettings.buttonText'))"
    i18n-path="dcis.grid.rowSettings"
    mutation-name="changeRowDimension"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="String(t('dcis.grid.rowSettings.height'))"
        rules="required|integer|min_value:0"
      )
        v-text-field(
          v-model="height"
          :error-messages="errors"
          :success="valid"
          :label="t('dcis.grid.rowSettings.height')"
        )
      v-checkbox(v-model="fixed" :label="t('dcis.grid.rowSettings.fix')" success)
      v-checkbox(v-model="hidden" :label="t('dcis.grid.rowSettings.hide')" success)
      v-checkbox(
        v-model="dynamic"
        :label="t('dcis.grid.rowSettings.makeDynamic')"
        :disabled="!!row.children.length"
        success
      )
</template>

<script lang="ts">
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { PropType } from '#app'
import { UpdateType } from '~/composables'
import {
  SheetQuery,
  RowDimensionType,
  RowDimensionFieldsFragment,
  ChangeRowDimensionMutation,
  ChangeRowDimensionMutationVariables
} from '~/types/graphql'
import changeRowMutation from '~/gql/dcis/mutations/sheet/change_row_dimension.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    row: { type: Object as PropType<RowDimensionType>, required: true },
    getRowHeight: { type: Function as PropType<(row: RowDimensionType) => number>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { dateTimeHM } = useFilters()

    const height = ref<number>(props.getRowHeight(props.row))
    const fixed = ref<boolean>(props.row.fixed)
    const hidden = ref<boolean>(props.row.hidden)
    const dynamic = ref<boolean>(props.row.dynamic)

    const variables = computed<ChangeRowDimensionMutationVariables>(() => ({
      rowDimensionId: props.row.id,
      height: height.value,
      fixed: fixed.value,
      hidden: hidden.value,
      dynamic: dynamic.value
    }))

    const optimisticResponse = computed<ChangeRowDimensionMutation>(() => ({
      __typename: 'Mutation',
      changeRowDimension: {
        __typename: 'ChangeRowDimensionMutationPayload',
        success: true,
        errors: [],
        rowDimensionId: variables.value.rowDimensionId,
        height: variables.value.height,
        fixed: variables.value.fixed,
        hidden: variables.value.hidden,
        dynamic: variables.value.dynamic
      }
    }))

    const updateSheet = inject<UpdateType<SheetQuery>>('updateActiveSheet')

    const update = (dataProxy: DataProxy, result: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>) => {
      updateSheet(
        dataProxy,
        result,
        (
          data: SheetQuery,
          { data: { changeRowDimension } }: Omit<FetchResult<ChangeRowDimensionMutation>, 'context'>
        ) => {
          if (changeRowDimension.success) {
            const rowDimension = data.sheet.rows.find((rowDimension: RowDimensionFieldsFragment) =>
              rowDimension.id === changeRowDimension.rowDimensionId)!
            rowDimension.height = changeRowDimension.height
            rowDimension.fixed = changeRowDimension.fixed
            rowDimension.hidden = changeRowDimension.hidden
            rowDimension.dynamic = changeRowDimension.dynamic
          }
          return data
        }
      )
    }

    return {
      t,
      dateTimeHM,
      height,
      fixed,
      hidden,
      dynamic,
      variables,
      optimisticResponse,
      update,
      changeRowMutation
    }
  }
})
</script>
