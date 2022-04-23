<template lang="pug">
  .grid__cell-content(:class="contentClasses")
    component(
      v-if="active && cell.editable"
      @set-value="setCellValue"
      @cancel="$emit('clear-active')"
      :value-type="cell.valueType"
      :value="cell.value"
      :is="`GridCell${cellKind}`"
    )
    template(v-else-if="cell.kind === 'fl'")
      grid-cell-file-value(:value-type="cell.valueType" :value="cell.value")
    template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { FetchResult } from '@apollo/client/link/core'
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, inject } from '#app'
import { BuildCellType } from '~/types/grid-types'
import { cellKinds } from '~/composables/grid'
import {
  DocumentQuery,
  ValueType,
  ChangeValueMutation,
  ChangeFileValueMutation,
  ChangeValueMutationVariables,
  ChangeFileValueMutationVariables
} from '~/types/graphql'
import changeValueMutation from '~/gql/dcis/mutations/document/change_value.graphql'
import changeFileValueMutation from '~/gql/dcis/mutations/document/change_file_value.graphql'
import GridCellNumeric from '~/components/dcis/grid/cells/GridCellNumeric.vue'
import GridCellString from '~/components/dcis/grid/cells/GridCellString.vue'
import GridCellText from '~/components/dcis/grid/cells/GridCellText.vue'
import GridCellFiles from '~/components/dcis/grid/cells/GridCellFiles.vue'
import GridCellMoney from '~/components/dcis/grid/cells/GridCellMoney.vue'
import GridCellDepartment from '~/components/dcis/grid/cells/GridCellDepartment.vue'
import GridCellUser from '~/components/dcis/grid/cells/GridCellUser.vue'
import GridCellFileValue from '~/components/dcis/grid/values/GridCellFileValue.vue'

export type ChangeValueMutationResult = { data: ChangeValueMutation }
export type ChangeFileValueMutationResult = { data: ChangeFileValueMutation }

type ChangeValueDocumentUpdateType = (
  cache: DataProxy,
  result: ChangeValueMutationResult | ChangeFileValueMutationResult,
  transform: (dc: DocumentQuery, r: ChangeValueMutationResult | ChangeFileValueMutationResult) => DocumentQuery
) => DataProxy

export default defineComponent({
  components: {
    GridCellNumeric,
    GridCellString,
    GridCellText,
    GridCellFiles,
    GridCellMoney,
    GridCellDepartment,
    GridCellUser,
    GridCellFileValue
  },
  props: {
    cell: { type: Object as PropType<BuildCellType>, required: true },
    active: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const cellKind: ComputedRef<string> = computed<string>(() => (
      props.cell.kind in cellKinds ? cellKinds[props.cell.kind] : 'String'
    ))

    const contentClasses: ComputedRef<Record<string, boolean>> = computed<Record<string, boolean>>(() => ({
      'grid__cell-content_active': props.active && ['n', 's', 'money'].includes(props.cell.kind)
    }))

    const documentId: string = inject<string>('documentId')
    const documentUpdate: ChangeValueDocumentUpdateType = inject<ChangeValueDocumentUpdateType>('documentUpdate')
    const updateValue = (dataCache: DocumentQuery, value: ValueType) => {
      const values: ValueType[] = dataCache.document.sheets!
        .find(sh => sh.id === props.cell.sheetId)
        .values.filter((v: ValueType) => v.id !== value.id)
      dataCache.document.sheets!.find(sh => sh.id === props.cell.sheetId)!.values = [...values, value] as any
      return dataCache
    }
    const { mutate: changeValueMutate } = useMutation<
      ChangeValueMutation,
      ChangeValueMutationVariables
    >(changeValueMutation)
    const { mutate: changeFileValueMutate } = useMutation<
      ChangeFileValueMutation,
      ChangeFileValueMutationVariables
    >(changeFileValueMutation)

    const setCellValue = (
      value: string,
      args: any,
      additionalUpdate: <TResultMutation>(
        cache: DataProxy,
        result: Omit<FetchResult<TResultMutation>, 'context'>
      ) => void | null = null
    ) => {
      if (props.cell.kind === 'fl') {
        changeFileValueMutate({
          documentId,
          sheetId: +props.cell.sheetId,
          columnId: props.cell.cell.columnId,
          rowId: props.cell.cell.rowId,
          value,
          ...args
        }, {
          update: (cache, result) => {
            const dataProxy = cache as unknown as DataProxy
            documentUpdate(
              dataProxy,
              result as ChangeFileValueMutationResult,
              (
                dataCache: DocumentQuery,
                { data: { changeFileValue: { success, value } } }: ChangeFileValueMutationResult
              ) => {
                return success ? updateValue(dataCache, value) : dataCache
              }
            )
            additionalUpdate!(dataProxy, result)
          }
        })
      } else if (props.cell.value !== value) {
        changeValueMutate({
          documentId,
          sheetId: +props.cell.sheetId,
          columnId: props.cell.cell.columnId,
          rowId: props.cell.cell.rowId,
          value
        }, {
          update: (cache, result) => documentUpdate(
            cache as unknown as DataProxy,
            result as ChangeValueMutationResult,
            (
              dataCache: DocumentQuery,
              { data: { changeValue: { success, value } } }: ChangeValueMutationResult
            ) => {
              return success ? updateValue(dataCache, value) : dataCache
            }
          )
        })
      }
      emit('clear-active')
    }

    return { cellKind, contentClasses, setCellValue }
  }
})
</script>
