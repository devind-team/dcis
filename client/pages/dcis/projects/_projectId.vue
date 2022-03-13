<template lang="pug">
  div
    left-navigator-driver(v-model="drawer" :items="links")
    v-progress-circular(v-if="loading" color="primary" indeterminate)
    nuxt-child(v-else :breadCrumbs="bc" :project="project")
</template>

<script lang="ts">
import type { Ref, ComputedRef } from '#app'
import { computed, defineComponent, PropType, provide, ref, useRoute } from '#app'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useCommonQuery, useI18n } from '~/composables'
import { ProjectQuery, ProjectQueryVariables } from '~/types/graphql'
import projectQuery from '~/gql/dcis/queries/project.graphql'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'

export default defineComponent({
  components: { LeftNavigatorDriver },
  middleware: 'auth',
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { localePath } = useI18n()
    const route = useRoute()
    const drawer: Ref<boolean> = ref<boolean>(false)
    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      { title: 'Периоды', to: 'dcis-projects-projectId-periods', icon: 'file-table-box-multiple-outline' },
      { title: 'Пользователи', to: 'dcis-projects-projectId-accounts', icon: 'account-wrench', permissions: 'core.view_experimental' },
      {
        title: 'Настройки',
        to: 'dcis-projects-projectId-settings',
        icon: 'cogs',
        permissions: ['dcis.change_project', 'dcis.delete_project'],
        permOr: true
      }
    ]))
    const { data: project, loading, update } = useCommonQuery<ProjectQuery, ProjectQueryVariables>({
      document: projectQuery,
      variables: () => ({
        projectId: route.params.projectId
      })
    })
    provide('projectUpdate', update)
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      if (loading.value) {
        return props.breadCrumbs
      }
      return [
        ...props.breadCrumbs,
        {
          text: project.value.name,
          to: localePath({ name: 'dcis-projects-projectId-periods', params: route.params }),
          exact: true
        }
      ]
    })
    return { bc, drawer, links, project, loading }
  }
})
</script>
