<template lang="pug">
v-dialog(v-model="active" width="50vw" )
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attrs="attrs")
  v-card
    v-card-title {{ $t('dcis.sheets.settings.show') }}
      v-spacer
      v-btn(@click="close" icon)
        v-icon mdi-close
    v-card-text
      v-data-table(:headers="headers" :items="sheets" dense disable-sort disable-pagination hide-default-footer)
        template(v-for="show in shows" v-slot:[`item.${show}`]="{ item }")
          v-checkbox(:input-value="item[show]" @change="mutate({ sheetId: item.id, field: show, value: $event })" dense)
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import { computed, defineComponent, inject, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify/types'
import { FetchResult } from '@apollo/client/link/core'
import { TransformUpdate, useI18n } from '~/composables'
import {
  BaseSheetType,
  ChangeShowSheetMutation, ChangeShowSheetMutationPayload,
  ChangeShowSheetMutationVariables, PeriodQuery
} from '~/types/graphql'
import changeShowSheetMutation from '~/gql/dcis/mutations/period/change_show_sheet.graphql'

export default defineComponent({
  props: {
    sheets: { type: Array as PropType<BaseSheetType[]>, required: true }
  },
  setup (_, { emit }) {
    const { t } = useI18n()
    const active = ref<boolean>(false)
    const shows: string[] = ['showHead', 'showChild']
    const headers = computed<DataTableHeader[]>(() => (['name', ...shows].map((h: string) => ({
      text: t(`dcis.sheets.settings.${h}`) as string,
      value: h
    }))))

    const periodUpdate = inject<(
      cache: DataProxy,
      result: Omit<FetchResult<ChangeShowSheetMutation>, 'context'>,
      transform: TransformUpdate<PeriodQuery, { data: { changeShowSheet: ChangeShowSheetMutationPayload }}>
    ) => void>('periodUpdate')

    const { mutate } = useMutation<ChangeShowSheetMutation, ChangeShowSheetMutationVariables>(changeShowSheetMutation, {
      update: (cache: DataProxy | any, result: Omit<FetchResult<ChangeShowSheetMutation>, 'context'>) => {
        const { success, sheet } = result.data.changeShowSheet
        if (success) {
          periodUpdate(cache, result, (dataCache) => {
            const index = dataCache.period.sheets.map((s: BaseSheetType) => s.id).indexOf(sheet.id)
            dataCache.period.sheets.splice(index, 1, sheet)
            return dataCache
          })
        }
      }
    })

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, shows, headers, mutate, close }
  }
})
</script>
