<template lang="pug">
  v-card(flat)
    v-card-text
      v-data-table(
        :value="selectDivisions"
        @input="changeDivisions"
        :headers="headers"
        :items="divisions"
        :loading="loading"
        disable-pagination
        hide-default-footer
        show-select
      )
        template(#item.name="{ item }") {{ item.name }}
        template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { computed, ComputedRef, defineComponent, inject, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import { useFilters } from '~/composables'
import {
  ActionRelationShip,
  DivisionType,
  PeriodType,
  ChangeDivisionsMutation,
  ChangeDivisionsMutationPayload,
  ChangeDivisionsMutationVariables
} from '~/types/graphql'
import changeDivisionsMutation from '~/gql/dcis/mutations/project/change_divisions.graphql'

type ChangeDivisionsResultMutation = { data: { changeDivisions: ChangeDivisionsMutationPayload } }
type ChangeDivisionsUpdateType = (cache: any, result: ChangeDivisionsResultMutation | any, transform: (dc: any, r: ChangeDivisionsResultMutation) => any) => DataProxy

export default defineComponent({
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    divisions: { type: Array as PropType<any>, default: () => ([]) },
    loading: { type: Boolean as PropType<boolean>, required: true }
  },
  setup (props) {
    const { dateTimeHM } = useFilters()
    const selectDivisions: ComputedRef<any[]> = computed<any[]>(():any => {
      return props.divisions.filter(division => props.period.divisions.map(e => e.objectId).includes(Number(division.id)))
    })
    const periodUpdate: ChangeDivisionsUpdateType = inject<ChangeDivisionsUpdateType>('changeUpdate')
    const { mutate: ChangeDivisionsMutate } = useMutation<ChangeDivisionsMutation, ChangeDivisionsMutationVariables>(
      changeDivisionsMutation,
      {
        update: (cache, result) => periodUpdate(cache, result,
          (dataCache, { data: { changeDivisions: { success, divisionsId, action } } }): any => {
            if (success) {
              const dataKey: string = Object.keys(dataCache)[0]
              if (action === 'ADD') {
                dataCache[dataKey][props.period.id].divisions.push(
                  ...props.period.divisions.filter(e => divisionsId.includes(Number(e.id)))
                )
              } else if (action === 'DELETE') {
                dataCache[dataKey][props.period.id].divisions = dataCache[dataKey][props.period.id].divisions.filter(
                  (el: DivisionType) => !divisionsId.includes(Number(el.id))
                )
              }
            }
            return dataCache
          })
      })
    const changeDivisions = (divisions: DivisionType[]): void => {
      if (divisions.length === selectDivisions.value.length) { return }
      let diff: DivisionType[]
      let action: string
      if (divisions.length > selectDivisions.value.length) {
        diff = divisions.filter((e: DivisionType) => !selectDivisions.value.map((el: DivisionType) => el.id).includes(e.id))
        action = 'ADD'
      } else {
        diff = selectDivisions.value.filter((e: DivisionType) => !divisions.map((el: DivisionType) => el.id).includes(e.id))
        action = 'DELETE'
      }
      const divisionsId: number[] = diff.map((e: DivisionType) => Number(e.id))
      ChangeDivisionsMutate({
        periodId: props.period.id,
        divisionsId,
        action: (action as ActionRelationShip)
      })
    }
    const headers: DataTableHeader[] = [
      { text: 'Название объекта', value: 'name' },
      { text: 'Дата создания', value: 'createdAt' }
    ]
    return { headers, dateTimeHM, changeDivisions, selectDivisions }
  }
})
</script>
