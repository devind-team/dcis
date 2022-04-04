<template lang="pug">
  div
    left-navigator-driver(v-model="drawer" :items="links")
    v-progress-circular(v-if="loading" color="primary" indeterminate)
    nuxt-child(v-else  @update-drawer="drawer = !drawer" :breadCrumbs="bc" :period="period")
</template>

<script lang="ts">
import type { Ref, ComputedRef, PropType } from '#app'
import { computed, defineComponent, ref, useRoute, provide } from '#app'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useCommonQuery, useI18n } from '~/composables'
import { PeriodQuery, PeriodQueryVariables } from '~/types/graphql'
import periodQuery from '~/gql/dcis/queries/period.graphql'
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
      { title: 'Документ', to: 'dcis-periods-periodId-documents', icon: 'file-table-box-multiple-outline' },
      { title: 'Объекты', to: 'dcis-periods-periodId-divisions', icon: 'briefcase-outline' },
      { title: 'Атрибуты', to: 'dcis-periods-periodId-attributes', icon: 'format-list-text', permissions: 'core.view_experimental' },
      {
        title: 'Настройки',
        to: 'dcis-periods-periodId-settings',
        icon: 'cogs',
        permissions: ['dcis.change_period', 'dcis.delete_period'],
        permOr: true
      }
    ]))
    const {
      data: period,
      loading,
      update,
      changeUpdate
    } = useCommonQuery<PeriodQuery, PeriodQueryVariables>({
      document: periodQuery,
      variables: () => ({
        periodId: route.params.periodId
      })
    })
    provide('periodUpdate', update)
    provide('changeUpdate', changeUpdate)
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      if (loading.value) {
        return props.breadCrumbs
      }
      return [
        ...props.breadCrumbs,
        {
          text: period.value.project.name,
          to: localePath({ name: 'dcis-projects-projectId-periods', params: { projectId: period.value.project.id } }),
          exact: true
        },
        { text: period.value.name, to: localePath({ name: 'dcis-periods-periodId-documents' }), exact: true }
      ]
    })
    return { bc, drawer, links, period, loading }
  }
})
</script>
