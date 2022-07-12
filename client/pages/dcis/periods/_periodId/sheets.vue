<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.sheets.name') }}
  v-row
    v-col(cols="12")
      v-tabs
        template(v-for="sheet in period.sheets")
          sheet-control(v-slot="{ on, attrs }" :sheet="sheet" :update="renameSheetUpdate" :key="sheet.id")
            v-tab(v-bind="attrs" @contextmenu.prevent="on.click") {{ sheet.name }}
      v-tabs-items(v-model="activeSheetIndex")
        v-tab-item(v-for="sheet in period.sheets" :key="sheet.id")
          div {{ activeSheet }}
</template>

<script lang="ts">
import { ApolloCache } from '@apollo/client'
import { FetchResult } from '@apollo/client/link/core'
import { inject, PropType, ref } from '#app'
import { UpdateType } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  SheetType,
  PeriodQuery,
  DocumentsSheetQuery,
  DocumentsSheetQueryVariables,
  RenameSheetMutation
} from '~/types/graphql'
import documentsSheetQuery from '~/gql/dcis/queries/documents_sheet.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import SheetControl from '~/components/dcis/grid/controls/SheetControl.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, SheetControl },
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
      changeUpdate
    } = useCommonQuery<
      DocumentsSheetQuery,
      DocumentsSheetQueryVariables
    >({
      document: documentsSheetQuery,
      variables: () => ({
        sheetId: props.period.sheets[activeSheetIndex.value].id,
        documentIds: []
      })
    })

    const renameSheetUpdate = (cache: ApolloCache<RenameSheetMutation>, result: FetchResult<RenameSheetMutation>) => {
      if (result.data.renameSheet.success) {
        periodUpdate(
          cache,
          result,
          (dataCache, { data: { renameSheet: { sheet } } }: FetchResult<RenameSheetMutation>) => {
            dataCache.period.sheets.find(periodSheet => periodSheet.id === sheet.id).name = sheet.name
            return dataCache
          }
        )
      }
    }

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      bc,
      activeSheetIndex,
      activeSheet,
      updateActiveSheet,
      renameSheetUpdate
    }
  }
})
</script>
