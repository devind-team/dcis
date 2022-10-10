<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  h2 {{ divisions }}
  v-card
    v-card-title {{ $t('dcis.projects.name') }}
      template(v-if="hasPerm('dcis.add_project')")
        v-spacer
        add-project(:update="(cache, result) => addUpdate(cache, result, 'project')")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") {{ $t('dcis.projects.addProject.buttonText') }}
    v-card-subtitle {{ $t('shownOf', { count: visibleProjects.length, totalCount }) }}
    v-card-text
      items-data-filter(
        v-model="selectedFilters"
        :items="filterOptions"
        :get-name="i => i.tr"
        :no-filtration-message="String($t('dcis.projects.filters.noFiltrationMessage'))"
        :default-value="[defaultFilter]"
        item-key="key"
        multiple
      )
      v-data-table(
        :headers="headers"
        :items="projects"
        :loading="loading"
        disable-pagination
        disable-filtering
        hide-default-footer
      )
        template(#item.name="{ item }")
          nuxt-link(
            :to="localePath({ name: 'dcis-projects-projectId-periods', params: { projectId: item.id } })"
          ) {{ item.name }}
        template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import { computed, defineComponent, onMounted, ref, toRef, useNuxt2Meta, useRoute, useRouter } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useApolloHelpers, useFilters, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import { useProjects } from '~/services/grapqhl/queries/dcis/projects'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import AddProject from '~/components/dcis/projects/AddProject.vue'

export default defineComponent({
  name: 'DcisProjects',
  components: { AddProject, BreadCrumbs, ItemsDataFilter },
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
    const { dateTimeHM, getUserFullName } = useFilters()
    useNuxt2Meta({ title: t('dcis.home') as string })
    const active = ref<boolean>(false)
    const name = ref<string>('')
    const headers: DataTableHeader[] = [
      { text: t('dcis.projects.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.projects.tableHeaders.description') as string, value: 'description' },
      { text: t('dcis.projects.tableHeaders.createdAt') as string, value: 'createdAt' }
    ]
    const user = toRef(authStore, 'user')
    const hasPerm = toRef(authStore, 'hasPerm')

    const divisions = computed<string>(() => (
      user.value.divisions && user.value.divisions.length
        ? user.value.divisions.map(d => `${d.name} (${d.id})`).join(', ')
        : getUserFullName(user)
    ))

    const {
      data: projects,
      pagination: { count, totalCount },
      loading,
      addUpdate,
      deleteUpdate
    } = useProjects()

    const defaultFilter = { key: 'active', tr: t('dcis.projects.filters.active') }

    const filterOptions = ref([
      defaultFilter,
      { key: 'archive', tr: t('dcis.projects.filters.archive') }
    ])

    if (projects.value.find(x => !x.visibility)) {
      filterOptions.value.push({ key: 'hidden', tr: t('dcis.projects.filters.hidden') })
    }

    const selectedFilters = ref([defaultFilter])

    const visibleProjects = computed(() => {
      const filterKeys = selectedFilters.value.map(x => x.key)
      return projects.value.filter((x) => {
        return (!x.visibility && filterKeys.includes('hidden')) ||
          (x.archive && filterKeys.includes('archive')) ||
          (!x.archive && x.visibility && filterKeys.includes('active'))
      })
    })

    onMounted(() => {
      if (route.query.deleteProjectId) {
        deleteUpdate(defaultClient.cache, { data: { deleteProject: { id: route.query.deleteProjectId } } })
        router.push(localePath({ name: 'dcis-projects' }))
      }
    })

    return {
      hasPerm,
      active,
      name,
      headers,
      projects,
      filterOptions,
      selectedFilters,
      visibleProjects,
      divisions,
      count,
      totalCount,
      loading,
      defaultFilter,
      dateTimeHM,
      addUpdate
    }
  }
})
</script>
