<template lang="pug">
bread-crumbs(v-if="user.divisions.length" :items="breadCrumbs")
  v-card
    v-tabs(grow)
      v-tab {{ $t('dcis.projects.name') }}
      v-tab {{ $t('dcis.projects.divisions') }}
      v-tab-item
        v-card(flat)
          v-card-text
            .d-flex
              div {{ $t('shownOf', { count: projects.length, totalCount }) }}
              template(v-if="hasPerm('dcis.add_project')")
                v-spacer
                add-project(:update="(cache, result) => addUpdate(cache, result, 'project')")
                  template(#activator="{ on }")
                    v-btn(v-on="on" color="primary") {{ $t('dcis.projects.addProject.buttonText') }}
            projects-filter(v-model="selectedFilters" :default-value="defaultFilter")
            v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
            projects-table(:projects="projects" :loading="loading")
      v-tab-item
        v-list
          v-list-item(v-for="division in user.divisions" :key="division.id")
            v-list-item-content {{ division.name }} ({{ division.id }})
left-navigator-container(v-else :bread-crumbs="breadCrumbs" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.projects.name') }}
    template(v-if="hasPerm('dcis.add_project')")
      v-spacer
      add-project(:update="(cache, result) => addUpdate(cache, result, 'project')")
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ $t('dcis.projects.addProject.buttonText') }}
  template(#subheader) {{ $t('shownOf', { count: projects.length, totalCount }) }}
  projects-filter(v-model="selectedFilters" :default-value="defaultFilter")
  v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
  projects-table(:projects="projects" :loading="loading")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { computed, defineComponent, onMounted, ref, toRef, useNuxt2Meta } from '#app'
import { useRoute, useRouter } from '#imports'
import { BreadCrumbsItem } from '~/types/devind'
import { ProjectsQuery, ProjectsQueryVariables, ProjectType } from '~/types/graphql'
import { Item } from '~/types/filters'
import { useApolloHelpers, useCursorPagination, useI18n, useQueryRelay } from '~/composables'
import { useAuthStore } from '~/stores'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import ProjectsFilter from '~/components/dcis/projects/ProjectsFilter.vue'
import AddProject from '~/components/dcis/projects/AddProject.vue'
import ProjectsTable from '~/components/dcis/projects/ProjectsTable.vue'
import projectsQuery from '~/gql/dcis/queries/projects.graphql'

export default defineComponent({
  name: 'DcisProjects',
  components: { LeftNavigatorContainer, BreadCrumbs, ProjectsFilter, AddProject, ProjectsTable },
  middleware: 'auth',
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup () {
    const authStore = useAuthStore()
    const router = useRouter()
    const route = useRoute()
    const { defaultClient } = useApolloHelpers()
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('dcis.home') as string })
    const active = ref<boolean>(false)
    const name = ref<string>('')
    const user = toRef(authStore, 'user')
    const hasPerm = toRef(authStore, 'hasPerm')

    const search = ref<string>('')

    const defaultFilter: Item[] = [{ id: 'active' }]
    const selectedFilters = ref<Item[]>([{ id: 'active' }])

    const projectQueryEnabled = ref<boolean>(false)
    const {
      data: projects,
      pagination: { count, totalCount },
      loading,
      addUpdate,
      deleteUpdate
    } = useQueryRelay<ProjectsQuery, ProjectsQueryVariables, ProjectType>({
      document: projectsQuery,
      variables: () => {
        const activeFilter = +!!selectedFilters.value.find(x => x.id === 'active')
        const hiddenFilter = +!!selectedFilters.value.find(x => x.id === 'hidden')
        const archiveFilter = !!selectedFilters.value.find(x => x.id === 'archive')

        if (!activeFilter && !hiddenFilter && !archiveFilter) {
          return {
            visibility: null,
            archived: null,
            search: search.value
          }
        }

        return {
          visibility: activeFilter ^ hiddenFilter ? activeFilter || false : null,
          archive: archiveFilter,
          search: search.value
        }
      },
      options: computed(() => ({
        enabled: projectQueryEnabled.value
      }))
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    onMounted(() => {
      projectQueryEnabled.value = true
      if (route.query.deleteProjectId) {
        deleteUpdate(
          defaultClient.cache,
          { data: { deleteProject: { id: route.query.deleteProjectId } } },
          false
        )
        router.push(localePath({ name: 'dcis-projects' }))
      }
    })

    return {
      search,
      hasPerm,
      active,
      name,
      projects,
      selectedFilters,
      count,
      totalCount,
      loading,
      defaultFilter,
      user,
      addUpdate
    }
  }
})
</script>
