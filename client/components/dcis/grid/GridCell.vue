<template lang="pug">
  .grid__cell-container(:class="{ 'grid__cell-container-active': activeContainer }" :style="cell.border")
    component(
      v-if="active && cell.editable"
      @set-value="setCellValue"
      @cancel="$emit('clear-active')"
      :value="cell.value"
      :is="`GridCell${cellKind}`"
    )
    template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { ApolloCache, DataProxy } from 'apollo-cache'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, inject } from '#app'
import { BuildCellType } from '~/types/grid-types'
import { cellKinds } from '~/composables/grid'
import { ChangeValueMutation, ChangeValueMutationVariables, DocumentQuery, ValueType } from '~/types/graphql'
import changeValueMutation from '~/gql/dcis/mutations/document/change_value.graphql'
import GridCellDepartment from '~/components/dcis/grid/cells/GridCellDepartment.vue'
import GridCellMoney from '~/components/dcis/grid/cells/GridCellMoney.vue'
import GridCellNumeric from '~/components/dcis/grid/cells/GridCellNumeric.vue'
import GridCellString from '~/components/dcis/grid/cells/GridCellString.vue'
import GridCellText from '~/components/dcis/grid/cells/GridCellText.vue'
import GridCellUser from '~/components/dcis/grid/cells/GridCellUser.vue'

export type ChangeValueMutationResult = { data: ChangeValueMutation }

type ChangeValueDocumentUpdateType = (
  cache: ApolloCache<DocumentQuery | any> | any,
  result: ChangeValueMutationResult | any,
  transform: (dc: DocumentQuery, r: ChangeValueMutationResult) => DocumentQuery
) => DataProxy

export default defineComponent({
  components: { GridCellUser, GridCellText, GridCellString, GridCellNumeric, GridCellMoney, GridCellDepartment },
  props: {
    cell: { type: Object as PropType<BuildCellType>, required: true },
    active: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const cellKind: ComputedRef<string> = computed<string>(() => (
      props.cell.kind in cellKinds ? cellKinds[props.cell.kind] : 'String'
    ))

    const activeContainer: ComputedRef<boolean> = computed<boolean>(() => (
      props.active && ['n', 's', 'money'].includes(props.cell.kind)
    ))

    const documentId: string = inject<string>('documentId')
    const documentUpdate: ChangeValueDocumentUpdateType = inject<ChangeValueDocumentUpdateType>('documentUpdate')
    const { mutate: changeValueMutate } = useMutation<ChangeValueMutation, ChangeValueMutationVariables>(changeValueMutation, {
      update: (cache, result) => documentUpdate(
        cache,
        result,
        (dataCache: DocumentQuery, { data: { changeValue: { success, value } } }: ChangeValueMutationResult) => {
          if (success) {
            const values: ValueType[] = dataCache.document.sheets!
              .find(sh => sh.id === props.cell.sheetId)
              .values.filter((v: ValueType) => v.id !== value.id)
            dataCache.document.sheets!.find(sh => sh.id === props.cell.sheetId)!.values = [...values, value] as any
          }
          return dataCache
        })
    })

    const setCellValue = (value: string) => {
      if (props.cell.value !== value) {
        changeValueMutate({
          documentId,
          sheetId: +props.cell.sheetId,
          columnId: props.cell.cell.columnId,
          rowId: props.cell.cell.rowId,
          value
        })
      }
      emit('clear-active')
    }

    return { cellKind, activeContainer, setCellValue }
  }
})
</script>
