<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    WaveContainer
      h2 {{ divisions }}
    v-card
      v-card-title {{ $t('dcis.home') }}
        template(v-if="hasPerm('dcis.add_project')")
          v-spacer
          add-project(:update="(cache, result) => addUpdate(cache, result, 'project')")
            template(#activator="{ on }")
              v-btn(v-on="on" color="primary") {{ $t('dcis.projects.addProject.header') }}
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
import type { PropType, Ref } from '#app'
import { computed, defineComponent, onMounted, ref, toRef, useNuxt2Meta, useRoute, useRouter } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useApolloHelpers, useFilters, useI18n } from '~/composables'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import { useUserDivisions } from '~/services/grapqhl/queries/dcis/divisions'
import { useProjects } from '~/services/grapqhl/queries/dcis/projects'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import AddProject from '~/components/dcis/projects/AddProject.vue'
import WaveContainer from '~/components/dcis/ui/WaveContainer.vue'
import { UserType } from '~/types/graphql'

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
    const active: Ref<boolean> = ref<boolean>(false)
    const name: Ref<string> = ref<string>('')
    const headers: DataTableHeader[] = [
      { text: 'Название', value: 'name' },
      { text: 'Описание', value: 'description' },
      { text: 'Дата добавления', value: 'createdAt' }
    ]
    const user: Ref<UserType> = toRef(authStore, 'user')
    const hasPerm: Ref<HasPermissionFnType> = toRef(authStore, 'hasPerm')

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
