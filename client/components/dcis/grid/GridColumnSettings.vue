<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String(t('dcis.grid.columnSettings.header'))"
    :subheader="String(t('dcis.grid.columnSettings.width', { width: column.width }))"
    :mutation="changeColumnDimensionMutation"
    :variables="{ id: column.id, hidden, fixed, kind: kind.value, width: column.width  }"
    :update="changeColumnDimensionUpdate"
    :button-text="String(t('dcis.grid.columnSettings.buttonText'))"
    i18n-path="dcis.documents.change.column"
    mutation-name="changeColumnDimension"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-combobox.mx-1(v-model="kind" :items="kinds" label="Тип")
      //- В разработке
      v-row
        v-col
          v-checkbox(v-model="fixed" :label="t('dcis.grid.columnSettings.fix')")
        v-col
          v-checkbox(v-model="hidden" :label="t('dcis.grid.columnSettings.hide')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { cellKinds } from '~/composables/grid'
import type { BuildColumnType } from '~/types/grid-types'
import type { ChangeColumnDimensionPayload, ColumnDimensionType } from '~/types/graphql'
import type { DocumentUpdateTransformType } from '~/components/dcis/Grid.vue'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

type ChangeColumnDimensionResultMutation = { data: ChangeColumnDimensionPayload }
type UpdateFunction = (
  cache: DataProxy,
  result: ChangeColumnDimensionResultMutation,
  transform: DocumentUpdateTransformType
) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    column: { type: Object as PropType<BuildColumnType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const fixed = ref<boolean>(props.column.fixed)
    const hidden = ref<boolean>(props.column.hidden)

    const kind = ref<{ text: string, value: string }>({
      text: t(`dcis.cellKinds.${props.column.kind}`) as string,
      value: props.column.kind
    })
    const kinds = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.cellKinds.${k}`) as string, value: k })))
    )

    const documentUpdate = inject<UpdateFunction>('documentUpdate')

    const changeColumnDimensionUpdate = (cache: DataProxy, result: ChangeColumnDimensionResultMutation) => {
      if (!result.data.errors.length) {
        documentUpdate(cache, result, (
          dataCache,
          { data: { columnDimension } }: ChangeColumnDimensionResultMutation
        ) => {
          const sheet = dataCache.document.sheets.find(sheet => sheet.id === props.column.sheetId)
          sheet.columns = sheet.columns.map((column: ColumnDimensionType) => (
            column.id === columnDimension.id ? Object.assign(column, columnDimension) : column
          ))
          return dataCache
        })
      }
    }

    return { t, fixed, hidden, kinds, kind, changeColumnDimensionMutation, changeColumnDimensionUpdate }
  }
})
</script>
