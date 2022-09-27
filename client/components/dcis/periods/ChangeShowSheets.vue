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
          v-checkbox(:input-value="item[show]")
    v-card-actions
      v-spacer
      v-btn(color="primary") {{ $t('save') }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify/types'
import { BaseSheetType } from '~/types/graphql'

export default defineComponent({
  props: {
    sheets: { type: Array as PropType<BaseSheetType[]>, required: true }
  },
  setup (_, { emit }) {
    const active = ref<boolean>(false)
    const shows: string[] = ['showHead', 'showChild']
    const headers = computed<DataTableHeader[]>(() => ([
      { text: 'Название листов', value: 'name' },
      { text: 'Показываем головам', value: 'showHead' },
      { text: 'Показываем филиалам', value: 'showChild' }
    ]))
    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, shows, headers, close }
  }
})
</script>
