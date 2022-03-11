<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-card
      v-card-title {{ $t('dcis.home') }}
        v-spacer
        v-dialog(v-model="active" width="600" )
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") Добавить проект сборов
          v-card
            v-card-title Добавление проекта
            v-card-text
              v-text-field(v-model="name" label="Название проекта")
            v-card-actions
              v-btn(@click="active = false") Закрыть
              v-spacer
              v-btn(@click="mutate({ name, short: name, description: `Описание ${name}` })" color="primary") Добавить
      v-card-subtitle {{ $t('shownOf', { count, totalCount }) }}
      v-card-text
        v-data-table(:headers="headers" :items="projects" :loading="loading" disable-pagination hide-default-footer)
          template(#item.name="{ item }")
            nuxt-link(
              :to="localePath({ name: 'dcis-projects-projectId', params: { projectId: item.id } })"
            ) {{ item.name }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import type { PropType, Ref } from '#app'
import { defineComponent, useNuxt2Meta, ref } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useCursorPagination, useI18n, useQueryRelay } from '~/composables'
import projectsQuery from '~/gql/dcis/queries/projects.graphql'
import addProjectMutation from '~/gql/dcis/mutations/project/add_project.graphql'
import {
  AddProjectMutation,
  AddProjectMutationVariables,
  ProjectsQuery,
  ProjectsQueryVariables,
  ProjectType
} from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'auth',
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup () {
    const { t } = useI18n()
    useNuxt2Meta({ title: t('dcis.home') as string })
    const active: Ref<boolean> = ref<boolean>(false)
    const name: Ref<string> = ref<string>('')
    const headers: DataTableHeader[] = [
      { text: 'Название', value: 'name' },
      { text: 'Описание', value: 'description' }
    ]

    const {
      data: projects,
      pagination: { count, totalCount },
      loading,
      addUpdate
    } = useQueryRelay<ProjectsQuery, ProjectsQueryVariables, ProjectType>({
      document: projectsQuery
    }, {
      pagination: useCursorPagination()
    })

    const { mutate, onDone } = useMutation<AddProjectMutation, AddProjectMutationVariables>(addProjectMutation, {
      update: (cache, result) => addUpdate(cache, result, 'project')
    })
    onDone(() => { active.value = false })

    return {
      active,
      name,
      headers,
      projects,
      count,
      totalCount,
      loading,
      mutate
    }
  }
})
</script>
