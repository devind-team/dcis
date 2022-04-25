<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :header="String($t('dcis.documents.change.column.header'))"
    :subheader="`Ширина: ${column.width}px`"
    :mutation="changeColumnDimensionMutation"
    :variables="{ id: column.id, hidden, fixed, kind: kind.value, width: column.width  }"
    :update="changeColumnDimensionUpdate"
    :button-text="String($t('dcis.documents.change.column.buttonText'))"
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
          v-checkbox(v-model="fixed" :label="$t('dcis.documents.change.column.fixed')")
        v-col
          v-checkbox(v-model="hidden" :label="$t('dcis.documents.change.column.hidden')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType, ComputedRef } from '#app'
import { computed, defineComponent, inject, ref } from '#app'
import { useI18n } from '~/composables'
import { cellKinds } from '~/composables/grid'
import changeColumnDimensionMutation from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'
import { BuildColumnType } from '~/types/grid-types'
import { ChangeColumnDimensionPayload, ColumnDimensionType } from '~/types/graphql'
import type { DocumentUpdateTransformType } from '~/components/dcis/Grid.vue'
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
    const kinds: ComputedRef<{ text: string, value: string }[]> = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.cellKinds.${k}`) as string, value: k })))
    )

    const documentUpdate = inject<UpdateFunction>('documentUpdate')

    const changeColumnDimensionUpdate = (cache: DataProxy, result: ChangeColumnDimensionResultMutation) => {
      if (!result.data.errors.length) {
        documentUpdate(cache, result, (dataCache, { data: { columnDimension } }: ChangeColumnDimensionResultMutation) => {
          const sheet = dataCache.document.sheets.find(sheet => sheet.id === props.column.sheetId)
          sheet.columns = sheet.columns.map((column: ColumnDimensionType) => (
            column.id === columnDimension.id ? Object.assign(column, columnDimension) : column
          ))
          return dataCache
        })
      }
    }

    return { fixed, hidden, kinds, kind, changeColumnDimensionMutation, changeColumnDimensionUpdate }
  }
})
</script>
