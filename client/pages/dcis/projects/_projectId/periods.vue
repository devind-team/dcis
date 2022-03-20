<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-card
      v-card-title Периоды
        v-spacer
        add-period(:update="addPeriodUpdate" :project="project")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Добавить сбор
      v-card-subtitle {{ project.name }}
      v-card-text
        v-data-table(:headers="headers" :items="project.periods" disable-pagination hide-default-footer)
          template(#item.name="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-periods-periodId-documents', params: { periodId: toGlobalId('PeriodType', item.id) } })"
            ) {{ item.name }}
          template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { Ref, PropType } from '#app'
import { defineComponent, inject, ref } from '#app'
import { useFilters } from '~/composables'
import { ProjectType } from '~/types/graphql'
import { toGlobalId } from '~/services/graphql-relay'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import AddPeriod, { AddPeriodMutationResult } from '~/components/dcis/projects/AddPeriod.vue'

export default defineComponent({
  components: { AddPeriod, BreadCrumbs },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup () {
    const { dateTimeHM } = useFilters()

    const name: Ref<string> = ref<string>('')
    const file: Ref<File | null> = ref<File | null>(null)

    const headers: DataTableHeader[] = [
      { text: '#', value: 'id' },
      { text: 'Название', value: 'name' },
      { text: 'Статус', value: 'status' },
      { text: 'Дата добавления', value: 'createdAt' }
    ]

    const projectUpdate: any = inject('projectUpdate')
    const addPeriodUpdate = (cache: DataProxy, result: AddPeriodMutationResult) => {
      projectUpdate(cache, result, (cacheData, { data: { addPeriod: { success, period } } }) => {
        if (success) {
          cacheData.project.periods = [period, ...cacheData.project.periods]
        }
        return cacheData
      })
    }
    return { name, file, headers, addPeriodUpdate, dateTimeHM, toGlobalId }
  }
})
</script>
