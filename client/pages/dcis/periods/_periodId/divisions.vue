<template lang="pug">
  left-navigator-container(:bread-crumbs="bc"  @update-drawer="$emit('update-drawer')")
    template(#header) {{ $t('dcis.periods.divisions.header') }}
    change-divisions(
      :period="period"
      :divisions="filterDivisions"
      :loading="loading"
      :update="changeDivisionsUpdate"
    )
      template(#activator="{ on }")
        v-btn(v-on="on" color="primary") {{ $t('dcis.periods.divisions.add') }}
    v-row(align="center")
      v-col(cols="12" md="8")
        v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right.pr-5(cols="12" md="4") {{ $t('dcis.periods.divisions.shownOf') }} {{ items.length }}
    v-card(flat)
      v-card-text
        v-data-table(
          :headers="headers"
          :items="items"
          :search.sync="search"
          :loading="loading"
          disable-pagination
          hide-default-footer
        )
          template(#item.action="{ item }")
            a(@click="deleteDivisionMutate(item.id)" style="color: #FF5252") {{ $t('dcis.periods.actions.delete') }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, inject } from '#app'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import {
  DeleteDivisionMutation,
  DeleteDivisionMutationVariables,
  DeleteDivisionsMutationPayload,
  DivisionsQuery,
  DivisionsQueryVariables,
  PeriodType
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useCommonQuery, useDebounceSearch, useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ChangeDivisions, { ChangeDivisionsMutationResult } from '~/components/dcis/periods/ChangeDivisions.vue'
import divisionsQuery from '~/gql/dcis/queries/divisions.graphql'
import deleteDivision from '~/gql/dcis/mutations/project/delete_division.graphql'

export type DeleteDivisionMutationResult = { data: { deleteDivision: DeleteDivisionsMutationPayload } }

export default defineComponent({
  components: { LeftNavigatorContainer, ChangeDivisions },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()
    const { search } = useDebounceSearch()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройка объектов сбора', to: localePath({ name: 'dcis-periods-periodId-divisions' }), exact: true }
    ]))
    const { t } = useI18n()
    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.id') as string, value: 'id', width: '10vw' },
      { text: t('dcis.periods.divisions.name') as string, value: 'name' },
      { text: t('dcis.periods.divisions.action') as string, value: 'action', width: '10vw' }
    ]
    const { mutate: DeleteDivisionMutation } = useMutation<DeleteDivisionMutation, DeleteDivisionMutationVariables>(
      deleteDivision,
      {
        update: (cache, result) => periodUpdate(
          cache, result, (dataCache, { data: { deleteDivision: { errors, deletedId } } }: DeleteDivisionMutationResult
          ) => {
            if (!errors.length) {
              dataCache.period.divisions = dataCache.period.divisions.filter((e: any) => e.id !== deletedId)
            }
            return dataCache
          })
      })
    const deleteDivisionMutate = (divisionId: string): void => {
      DeleteDivisionMutation({ id: props.period.divisions.find(e => e.objectId === Number(divisionId)).id })
    }
    const { data: divisions, loading } = useCommonQuery<DivisionsQuery, DivisionsQueryVariables>({
      document: divisionsQuery,
      variables: { periodId: props.period.id }
    })
    const items = computed<any>(() => {
      if (divisions.value) {
        return divisions.value.filter(division =>
          props.period.divisions.map(periodDivision => periodDivision.objectId).includes(Number(division.id)))
      } else {
        return []
      }
    })
    const filterDivisions = computed<any>(() => {
      if (divisions.value) {
        return divisions.value.filter(division =>
          !props.period.divisions.map(periodDivision => periodDivision.objectId).includes(Number(division.id)))
      } else {
        return []
      }
    })
    const periodUpdate: any = inject('periodUpdate')
    /**
     * Обновление после добавления объектов
     * @param cache
     * @param result
     */
    const changeDivisionsUpdate = (cache: DataProxy, result: ChangeDivisionsMutationResult) => {
      periodUpdate(
        cache, result, (dataCache, { data: { changeDivisions: { errors, divisions } } }: ChangeDivisionsMutationResult
        ) => {
          if (!errors.length) {
            dataCache.period.divisions = divisions
          }
          return dataCache
        })
    }
    return { bc, headers, changeDivisionsUpdate, filterDivisions, loading, divisions, search, items, deleteDivisionMutate }
  }
})
</script>
