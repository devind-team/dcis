<template lang="pug">
  left-navigator-container(:bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
    template(#header) Периоды
      template(v-if="hasPerm('dcis.add_period')")
        v-spacer
        add-period(:update="addPeriodUpdate" :project="project")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Добавить сбор
    v-data-table(:headers="headers" :items="project.periods" disable-pagination hide-default-footer)
      template(#item.name="{ item }")
        nuxt-link(
          :to="localePath({ name: 'dcis-periods-periodId-documents', params: { periodId: toGlobalId('PeriodType', item.id) } })"
        ) {{ item.name }}
      template(#item.status="{ item }") {{ statuses[item.status] }}
      template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { Ref, PropType } from '#app'
import { defineComponent, inject, onMounted, ref, useRoute, useRouter, toRef } from '#app'
import { useApolloHelpers, useFilters, useI18n } from '~/composables'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import { PeriodType, ProjectType } from '~/types/graphql'
import { toGlobalId } from '~/services/graphql-relay'
import { BreadCrumbsItem } from '~/types/devind'
import AddPeriod, { AddPeriodMutationResult } from '~/components/dcis/projects/AddPeriod.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, AddPeriod },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup () {
    const { t } = useI18n()
    const authStore = useAuthStore()
    const router = useRouter()
    const route = useRoute()
    const { dateTimeHM } = useFilters()
    const { localePath } = useI18n()
    const { defaultClient } = useApolloHelpers()

    const hasPerm: Ref<HasPermissionFnType> = toRef(authStore, 'hasPerm')
    const name: Ref<string> = ref<string>('')
    const file: Ref<File | null> = ref<File | null>(null)
    const statuses = Object.fromEntries(
      ['preparation', 'open', 'close'].map(e => ([e, t(`dcis.periods.statuses.${e}`) as string]))
    )
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

    return { name, file, headers, hasPerm, addPeriodUpdate, dateTimeHM, toGlobalId, statuses }
  }
})
</script>
