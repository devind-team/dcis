<template lang="pug">
v-expansion-panels(:value="Object.keys(settingsTree).map((k, i) => i)" flat multiple tile)
  v-expansion-panel(v-for="(values, key) in settingsTree" :key="key")
    v-expansion-panel-header {{ $t(`profile.settings.${key}`) }}
    v-expansion-panel-content
      v-data-table(
        :headers="headers"
        :items="values"
        hide-default-footer
        disable-pagination)
        template(#item.key="{ item }") {{ $t(`profile.settings.${item.key}`) }}
        template(#item.value="{ item }")
          v-switch(
            v-if="kindTypes[item.kindValue] === 'bool'"
            :key="item.key"
            @change="(e) => changeSettingValue(item.key, e)"
            :input-value="item.value" true-value="true" false-value="false")
          template(v-else) {{ item.value }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify/types'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { useI18n } from '~/composables'
import { SettingType } from '~/types/graphql'

export const kindTypes: { [key: string]: string } = {
  A_0: 'text',
  A_1: 'file',
  A_2: 'json',
  A_4: 'bool'
}

export default defineComponent({
  props: {
    settings: { type: Array as PropType<SettingType[]>, required: true },
    changeSettingValue: { type: Function as PropType<(key: string, value: string) => void>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('profile.tableHeaders.name') as string, value: 'key', width: '45%' },
      { text: t('profile.tableHeaders.value') as string, value: 'value', width: '55%' }
    ]))
    const settingsTree: ComputedRef<{ [k: string]: SettingType[] }> = computed<{ [k: string]: SettingType[] }>(() => (
      props.settings.reduce((grouped: { [key: string]: SettingType[] }, obj: SettingType) => {
        const keyValue: string = obj.key.split('_')[0]
        grouped[keyValue] = [...(grouped[keyValue] || []), obj]
        return grouped
      }, {})
    ))
    return { headers, kindTypes, settingsTree }
  }
})
</script>
