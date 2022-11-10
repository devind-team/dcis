<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.limitations.name') }}
    template(v-if="period.canChangeLimitations")
      v-spacer
      change-period-limitations-menu(
        :period="period"
        :from-file-update="limitationsResetUpdate"
        :add-update="limitationsAddUpdate"
      )
        template(#activator="{ on, attrs }")
          v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.periods.limitations.changeMenu.buttonText') }}
  template(#subheader) {{ $t('shownOf', { count, totalCount: count }) }}
  v-data-table(
    :headers="tableHeaders"
    :items="limitations"
    :loading="limitationsLoading"
    disable-pagination
    hide-default-footer
  )
</template>

<script lang="ts">
import { computed, defineComponent, useNuxt2Meta } from '#app'
import type { PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, LimitationsQuery, LimitationsQueryVariables } from '~/types/graphql'
import { useI18n, useCommonQuery } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import ChangePeriodLimitationsMenu from '~/components/dcis/periods/ChangePeriodLimitationsMenu.vue'
import limitationsQuery from '~/gql/dcis/queries/limitations.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, ChangePeriodLimitationsMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.limitations.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-limitations' }),
        exact: true
      }
    ]))

    const tableHeaders = computed<DataTableHeader[]>(() => [
      { text: t('dcis.periods.limitations.tableHeaders.sheet') as string, value: 'sheet.name' },
      { text: t('dcis.periods.limitations.tableHeaders.formula') as string, value: 'formula' },
      { text: t('dcis.periods.limitations.tableHeaders.errorMessage') as string, value: 'errorMessage' }
    ])

    const {
      data: limitations,
      loading: limitationsLoading,
      resetUpdate: limitationsResetUpdate,
      addUpdate: limitationsAddUpdate
    } = useCommonQuery<
      LimitationsQuery,
      LimitationsQueryVariables
    >({
      document: limitationsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })
    const count = computed<number>(() => limitations.value ? limitations.value.length : 0)

    return {
      bc,
      tableHeaders,
      limitations,
      limitationsLoading,
      limitationsResetUpdate,
      limitationsAddUpdate,
      count
    }
  }
})
</script>
