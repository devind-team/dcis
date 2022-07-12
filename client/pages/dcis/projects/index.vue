<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  wave-container
    h2 {{ divisions }}
  v-card
    v-card-title {{ $t('dcis.projects.name') }}
      template(v-if="hasPerm('dcis.add_project')")
        v-spacer
        add-project(:update="(cache, result) => addUpdate(cache, result, 'project')")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") {{ $t('dcis.projects.addProject.buttonText') }}
    v-card-subtitle {{ $t('shownOf', { count, totalCount }) }}
    v-card-text
      v-data-table(:headers="headers" :items="projects" :loading="loading" disable-pagination hide-default-footer)
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
import AddProject from '~/components/dcis/projects/AddProject.vue'
import WaveContainer from '~/components/dcis/ui/WaveContainer.vue'

export default defineComponent({
  components: { WaveContainer, AddProject, BreadCrumbs },
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

    onMounted(() => {
      if (route.query.projectId) {
        deleteUpdate(defaultClient.cache, { data: { deleteProject: { id: route.query.projectId } } })
        router.push(localePath({ name: 'dcis-projects' }))
      }
    })

    return {
      hasPerm,
      active,
      name,
      headers,
      projects,
      divisions,
      count,
      totalCount,
      loading,
      dateTimeHM,
      addUpdate
    }
  }
})
</script>
