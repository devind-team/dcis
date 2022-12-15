<template lang="pug">
bread-crumbs(v-if="user.divisions.length" :items="breadCrumbs")
  v-card
    v-tabs(grow)
      v-tab {{ $t('dcis.projects.name') }}
      v-tab(v-if="user.divisions.length") {{ $t('dcis.projects.divisions') }}
      v-tab-item
        v-card(flat)
          v-card-text
            .d-flex
              div {{ $t('shownOf', { count: visibleProjects.length, totalCount }) }}
              template(v-if="hasPerm('dcis.add_project')")
                v-spacer
                add-project(:update="(cache, result) => addUpdate(cache, result, 'project')")
                  template(#activator="{ on }")
                    v-btn(v-on="on" color="primary") {{ $t('dcis.projects.addProject.buttonText') }}
            projects-filter(v-model="selectedFilters" :default-value="defaultFilter" :projects="projects")
            projects-table(:projects="visibleProjects" :loading="loading")
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
  template(#subheader) {{ $t('shownOf', { count: visibleProjects.length, totalCount }) }}
  projects-filter(v-model="selectedFilters" :default-value="defaultFilter" :projects="projects")
  projects-table(:projects="visibleProjects" :loading="loading")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { computed, defineComponent, onMounted, ref, toRef, useNuxt2Meta } from '#app'
import { useRoute, useRouter } from '#imports'
import { BreadCrumbsItem } from '~/types/devind'
import { ProjectType } from '~/types/graphql'
import { Item } from '~/types/filters'
import { useApolloHelpers, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import { useProjects } from '~/services/grapqhl/queries/dcis/projects'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import ProjectsFilter from '~/components/dcis/projects/ProjectsFilter.vue'
import AddProject from '~/components/dcis/projects/AddProject.vue'
import ProjectsTable from '~/components/dcis/projects/ProjectsTable.vue'

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

    const {
      data: projects,
      pagination: { count, totalCount },
      loading,
      addUpdate,
      deleteUpdate
    } = useProjects()

    const defaultFilter: Item[] = [{ id: 'active' }]
    const selectedFilters = ref<Item[]>([{ id: 'active' }])

    const visibleProjects = computed<ProjectType[]>(() => {
      const filterKeys = selectedFilters.value.map(x => x.id)
      return projects.value.filter((x) => {
        return (!x.visibility && filterKeys.includes('hidden')) ||
          (x.archive && filterKeys.includes('archive')) ||
          (!x.archive && x.visibility && filterKeys.includes('active'))
      })
    })

    onMounted(() => {
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
      hasPerm,
      active,
      name,
      projects,
      selectedFilters,
      visibleProjects,
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
