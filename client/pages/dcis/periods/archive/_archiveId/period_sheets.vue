<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.sheets.name') }}
    v-spacer
    sheets-settings-menu(v-slot="{ on, attrs }" :sheets="period.sheets")
      v-btn(v-on="on" v-bind="attrs" icon)
        v-icon mdi-cog
  grid-sheets(
    v-model="activeSheetIndex"
    :mode="GridMode.READ"
    :sheets="period.sheets"
    :active-sheet="activeSheet"
    :loading="activeSheetLoading"
  )
    template(#tabs="{ sheets, updateSize }")
      template(v-for="sheet in sheets")
        sheet-control(
          v-slot="{ on, attrs }"
          :sheet="sheet"
          :key="sheet.id"
        )
          v-tab(v-bind="attrs" @contextmenu.prevent="on.click") {{ sheet.name }}
</template>

<script lang="ts">
import { computed, defineComponent, inject, PropType, ref } from '#app'
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
import SheetsSettingsMenu from '~/components/dcis/periods/SheetsSettingsMenu.vue'

export default defineComponent({
  components: { SheetsSettingsMenu, LeftNavigatorContainer, SheetControl, GridSheets },
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
        sheetId: props.period.sheets[activeSheetIndex.value].id
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
