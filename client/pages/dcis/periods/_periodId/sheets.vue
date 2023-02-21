<template lang="pug">
left-navigator-container.period-sheets__left-navigator-container(
  :bread-crumbs="bc"
  fluid
  @update-drawer="$emit('update-drawer')"
)
  template(#header) {{ $t('dcis.periods.sheets.name') }}
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.CHANGE"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
    :update-active-sheet="updateActiveSheet"
    :loading="activeSheetLoading"
  )
    template(#menus="{ selectedCellsOptions }")
      edit-menu(:mode="GridMode.CHANGE" :selected-cells-options="selectedCellsOptions")
      table-settings(:sheets="period.sheets")
    template(#tabs="{ sheets, updateSize }")
      template(v-for="sheet in sheets")
        sheet-control(
          v-slot="{ on, attrs }"
          :sheet="sheet" :update="(cache, result) => renameSheetUpdate(cache, result, updateSize)"
          :key="sheet.id"
        )
          v-tab.grid-sheet__tab(v-bind="attrs" @contextmenu.prevent="on.click") {{ sheet.name }}
</template>

<script lang="ts">
import { ApolloCache } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { computed, defineComponent, inject, PropType, ref } from '#app'
import { UpdateType, useCommonQuery, useI18n } from '~/composables'
import { GridMode } from '~/types/grid'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  PeriodQuery,
  PeriodSheetQuery,
  PeriodSheetQueryVariables,
  RenameSheetMutation
} from '~/types/graphql'
import periodSheetQuery from '~/gql/dcis/queries/period_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'
import GridSheets from '~/components/dcis/grid/GridSheets.vue'
import EditMenu from '~/components/dcis/grid/menus/EditMenu.vue'
import TableSettings from '~/components/dcis/grid/menus/TableSettingsMenu.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, SheetControl, GridSheets, EditMenu, TableSettings },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.sheets.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-sheets' }),
        exact: true
      }
    ]))

    const periodUpdate = inject<UpdateType<PeriodQuery>>('periodUpdate')

    const activeSheetIndex = ref<number>(0)
    const {
      data: activeSheet,
      update: updateActiveSheet,
      loading: activeSheetLoading
    } = useCommonQuery<
      PeriodSheetQuery,
      PeriodSheetQueryVariables
    >({
      document: periodSheetQuery,
      variables: () => ({
        sheetId: props.period.sheets[activeSheetIndex.value].id
      })
    })

    const renameSheetUpdate = (
      cache: ApolloCache<RenameSheetMutation>,
      result: FetchResult<RenameSheetMutation>,
      updateSize: () => void
    ) => {
      if (result.data.renameSheet.success) {
        periodUpdate(
          cache,
          result,
          (dataCache, { data: { renameSheet: { sheet } } }: FetchResult<RenameSheetMutation>) => {
            dataCache.period.sheets.find(periodSheet => periodSheet.id === sheet.id).name = sheet.name
            return dataCache
          }
        )
        updateSize()
      }
    }

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
      updateActiveSheet,
      activeSheetLoading,
      renameSheetUpdate
    }
  }
})
</script>

<style lang="sass">
.period-sheets__left-navigator-container
  .v-card__title
    padding-bottom: 8px
</style>
