<template lang="pug">
  v-card(flat)
    v-card-text
      v-data-table(
        :headers="headers"
        :items="divisions"
        :loading="loading"
        disable-pagination
        hide-default-footer
        show-select
      )
        template(#item.name="{ item }") {{ item.name }}
        template(#item.createdAt="{ item }") {{ item.createdAt }}
</template>

<script lang="ts">
import { defineComponent, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { PeriodType } from '~/types/graphql'

export default defineComponent({
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    divisions: { type: Array as PropType<any>, default: () => ([]) },
    loading: { type: Boolean as PropType<boolean>, required: true }
  },
  setup () {
    const headers: DataTableHeader[] = [
      { text: 'Название объекта', value: 'name' },
      { text: 'Дата создания', value: 'createdAt' }
    ]
    return { headers }
  }
})
</script>
