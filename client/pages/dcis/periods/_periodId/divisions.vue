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
    v-card(flat)
      v-card-text
        v-data-table(
          :headers="headers"
          :items="items"
          disable-pagination
          hide-default-footer
        )
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, inject } from '#app'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { DivisionsQuery, DivisionsQueryVariables, PeriodType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useCommonQuery, useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ChangeDivisions, { ChangeDivisionsMutationResult } from '~/components/dcis/periods/ChangeDivisions.vue'
import divisionsQuery from '~/gql/dcis/queries/divisions.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, ChangeDivisions },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройка объектов сбора', to: localePath({ name: 'dcis-periods-periodId-divisions' }), exact: true }
    ]))
    const { t } = useI18n()
    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.name') as string, value: 'name' }
    ]
    const { data: divisions, loading } = useCommonQuery<DivisionsQuery, DivisionsQueryVariables>({
      document: divisionsQuery,
      variables: { periodId: props.period.id }
    })
    const items = computed<any>(() => {
      if (divisions.value) {
        return divisions.value.filter(division => props.period.divisions.map(periodDivision => periodDivision.objectId).includes(Number(division.id)))
      } else {
        return []
      }
    })
    const filterDivisions = computed<any>(() => {
      if (divisions.value) {
        return divisions.value.filter(division => !props.period.divisions.map(periodDivision => periodDivision.objectId).includes(Number(division.id)))
      } else {
        return []
      }
    })
    const periodUpdate: any = inject('periodUpdate')
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
    return { bc, headers, changeDivisionsUpdate, filterDivisions, loading, divisions, items }
  }
})
</script>
