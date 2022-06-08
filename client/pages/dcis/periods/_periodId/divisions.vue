<template lang="pug">
  left-navigator-container(:bread-crumbs="bc"  @update-drawer="$emit('update-drawer')")
    template(#header) {{ $t('dcis.periods.divisions.header') }}
    change-divisions(
      :period="period"
    )
      template(#activator="{ on }")
        v-btn(v-on="on" color="primary") {{ $t('dcis.periods.divisions.add') }}
    v-card(flat)
      v-card-text
        v-data-table(
          :headers="headers"
          :items="period.divisions"
          disable-pagination
          hide-default-footer
        )
          template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, inject } from '#app'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { PeriodType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useFilters, useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ChangeDivisions, { ChangeDivisionsMutationResult } from '~/components/dcis/periods/ChangeDivisions.vue'

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
    const { dateTimeHM } = useFilters()
    const selectDivisions = computed<any[]>(():any => {
      return props.period.divisions
    })
    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.name') as string, value: 'name' },
      { text: t('dcis.periods.divisions.createdAt') as string, value: 'createdAt', width: 150 }
    ]
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
    return { bc, headers, selectDivisions, dateTimeHM }
  }
})
</script>
