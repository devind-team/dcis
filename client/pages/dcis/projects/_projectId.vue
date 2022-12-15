<template lang="pug">
div
  left-navigator-driver(v-model="drawer" :items="links")
  v-progress-circular(v-if="loading" color="primary" indeterminate)
  nuxt-child(v-else :breadCrumbs="bc" :project="project" @update-drawer="drawer = !drawer")
</template>

<script lang="ts">
import { computed, defineComponent, PropType, provide, ref } from '#app'
import { useRoute } from '#imports'
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
    const { t, localePath } = useI18n()

    const route = useRoute()

    const {
      data: project,
      loading,
      update,
      changeUpdate
    } = useCommonQuery<ProjectQuery, ProjectQueryVariables>({
      document: projectQuery,
      variables: () => ({
        projectId: route.params.projectId
      })
    })
    provide('projectUpdate', update)
    provide('changeUpdate', changeUpdate)

    const drawer = ref<boolean>(false)
    const links = computed<LinksType[]>(() => {
      const result: LinksType[] = [{
        title: t('dcis.projects.links.periods') as string,
        to: 'dcis-projects-projectId-periods',
        icon: 'file-table-box-multiple-outline'
      }]
      if (!loading.value && (project.value.canChange || project.value.canDelete)) {
        result.push({
          title: t('dcis.projects.links.settings') as string,
          to: 'dcis-projects-projectId-settings',
          icon: 'cogs'
        })
      }
      return result
    })

    const bc = computed<BreadCrumbsItem[]>(() => {
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

    return { project, loading, drawer, links, bc }
  }
})
</script>
