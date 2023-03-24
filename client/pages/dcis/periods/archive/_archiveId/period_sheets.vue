<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.sheets.name') }}
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.READ"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
    :loading="activeSheetLoading"
  )
</template>

<script lang="ts">
import { computed, defineComponent, useRoute, inject, PropType, ref } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  PeriodSheetQuery,
  PeriodSheetQueryVariables
} from '~/types/graphql'
import periodSheetQuery from '~/gql/dcis/queries/period_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, SheetControl, GridSheets },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.sheets.name') as string,
        to: localePath({ name: 'dcis-periods-archive-archiveId-period_sheets', query: route.query }),
        exact: true
      }
    ]))

    const activeSheetIndex = ref<number>(0)
    const {
      data: activeSheet,
      loading: activeSheetLoading
    } = useCommonQuery<
      PeriodSheetQuery,
      PeriodSheetQueryVariables
    >({
      document: periodSheetQuery,
      variables: () => ({
        sheetId: props.period.sheets[activeSheetIndex.value]?.id
      })
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      GridMode,
      bc,
      activeSheetIndex,
      activeSheet,
      activeSheetLoading
    }
  }
})
</script>
