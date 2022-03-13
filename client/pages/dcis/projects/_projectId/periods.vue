<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-card
      v-card-title Периоды
        v-spacer
        v-dialog(v-model="active" width="600")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Добавить новый сбор
          v-card
            v-card-title Добавить период
            v-card-subtitle {{ project.name }}
            v-card-text
              v-text-field(v-model="name" label="Название")
              v-file-input(v-model="file" label="Файл с формой сбора")
            v-card-actions
              v-btn(@click="active = false") Закрыть
              v-spacer
              v-btn(@click="mutate({ name, projectId: $route.params.projectId, file })" color="primary") Добавить период
      v-card-subtitle {{ project.name }}
      v-card-text
        v-data-table(:headers="headers" :items="project.periods" disable-pagination hide-default-footer)
          template(#item.name="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-periods-periodId', params: { periodId: toGlobalId('PeriodType', item.id) } })"
            ) {{ item.name }}
          template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import type { Ref, PropType } from '#app'
import { defineComponent, inject, ref } from '#app'
import { useFilters } from '~/composables'
import { AddPeriodMutation, AddPeriodMutationVariables, ProjectType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import addPeriodMutations from '~/gql/dcis/mutations/project/add_period.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { toGlobalId } from '~/services/graphql-relay'

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup () {
    const { dateTimeHM } = useFilters()

    const active: Ref<boolean> = ref<boolean>(false)
    const name: Ref<string> = ref<string>('')
    const file: Ref<File | null> = ref<File | null>(null)

    const headers: DataTableHeader[] = [
      { text: '#', value: 'id' },
      { text: 'Название', value: 'name' },
      { text: 'Статус', value: 'status' },
      { text: 'Дата добавления', value: 'createdAt' }
    ]

    const projectUpdate: any = inject('projectUpdate')
    const { mutate } = useMutation<AddPeriodMutation, AddPeriodMutationVariables>(addPeriodMutations, {
      update: (cache, result) => projectUpdate(cache, result, (cacheData, { data: { addPeriod: { success, period } } }) => {
        if (success) {
          active.value = false
          cacheData.project.periods = [period, ...cacheData.project.periods]
        }
        return cacheData
      })
    })
    return { active, name, file, headers, mutate, dateTimeHM, toGlobalId }
  }
})
</script>
