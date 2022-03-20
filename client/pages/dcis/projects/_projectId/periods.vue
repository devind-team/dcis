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
import { defineComponent, inject, onMounted, ref, useRoute, useRouter } from '#app'
import { useApolloHelpers, useFilters, useI18n } from '~/composables'
import { PeriodType, ProjectType } from '~/types/graphql'
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
    const router = useRouter()
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    const { localePath } = useI18n()
    const { defaultClient } = useApolloHelpers()

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

    onMounted(() => {
      if (route.query.periodId) {
        projectUpdate(
          defaultClient.cache,
          { data: { deletePeriod: { id: route.query.periodId } } },
          (cacheData, { data: { deletePeriod: { id: periodId } } }) => {
            cacheData.project.periods = cacheData.project.periods.filter((e: PeriodType) => e.id !== periodId)
            return cacheData
          }
        )
        router.push(localePath({ name: 'dcis-projects-projectId-periods', params: route.params }))
      }
    })

    return { name, file, headers, addPeriodUpdate, dateTimeHM, toGlobalId }
  }
})
</script>
