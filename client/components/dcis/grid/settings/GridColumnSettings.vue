<template lang="pug">
mutation-modal-form(
  :header="String(t('dcis.grid.columnSettings.header'))"
  :subheader="String(t('dcis.grid.columnSettings.subheader', { updatedAt: dateTimeHM(column.updatedAt) }))"
  :mutation="changeColumnDimensionMutation"
  :variables="variables"
  :optimistic-response="optimisticResponse"
  :update="update"
  :button-text="String(t('dcis.grid.columnSettings.buttonText'))"
  i18n-path="dcis.grid.columnSettings"
  mutation-name="changeColumnDimension"
  @close="$emit('close')"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String(t('dcis.grid.columnSettings.width'))"
      rules="required|integer|min_value:0"
    )
      v-text-field(
        v-model="width"
        :error-messages="errors"
        :success="valid"
        :label="t('dcis.grid.columnSettings.width')"
      )
    v-combobox.mx-1(v-model="kind" :items="kinds" :label="t('dcis.grid.columnSettings.kind')" color="primary")
    //- В разработке
    v-checkbox(v-model="fixed" :label="t('dcis.grid.columnSettings.fix')" color="primary")
    v-checkbox(v-model="hidden" :label="t('dcis.grid.columnSettings.hide')" color="primary")
</template>

<script lang="ts">
import { DataProxy } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { PropType, Ref } from '#app'
import { updateColumnDimension, UpdateType } from '~/composables'
import { cellKinds } from '~/composables/grid'
import {
  DocumentsSheetQuery,
  ColumnDimensionType,
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables
} from '~/types/graphql'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    column: { type: Object as PropType<ColumnDimensionType>, required: true },
    getColumnWidth: { type: Function as PropType<(column: ColumnDimensionType) => number>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { dateTimeHM } = useFilters()

    const width = ref<string>(String(props.getColumnWidth(props.column)))
    const fixed = ref<boolean>(props.column.fixed)
    const hidden = ref<boolean>(props.column.hidden)
    watch(computed<number>(() => props.getColumnWidth(props.column)), (newValue: number) => {
      width.value = String(newValue)
    })

    const kind = ref<{ text: string, value: string }>({
      text: t(`dcis.grid.cellKinds.${props.column.kind}`) as string,
      value: props.column.kind
    })
    const kinds = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.grid.cellKinds.${k}`) as string, value: k })))
    )

    const variables = computed<ChangeColumnDimensionMutationVariables>(() => ({
      columnDimensionId: props.column.id,
      width: +width.value,
      fixed: fixed.value,
      hidden: hidden.value,
      kind: kind.value.value
    }))
    const optimisticResponse = computed<ChangeColumnDimensionMutation>(() => ({
      __typename: 'Mutation',
      changeColumnDimension: {
        __typename: 'ChangeColumnDimensionMutationPayload',
        success: true,
        errors: [],
        ...variables.value,
        updatedAt: new Date().toISOString()
      }
    }))

    const updateSheet = inject<Ref<UpdateType<DocumentsSheetQuery>>>('updateActiveSheet')
    const update = (dataProxy: DataProxy, result: Omit<FetchResult<ChangeColumnDimensionMutation>, 'context'>) => {
      updateColumnDimension(updateSheet.value, dataProxy, result)
    }

    return {
      t,
      dateTimeHM,
      width,
      fixed,
      hidden,
      kinds,
      kind,
      variables,
      optimisticResponse,
      update,
      changeColumnDimensionMutation
    }
  }
})
</script>
