<template lang="pug">
  div
    left-navigator-driver(v-model="drawer" :items="links")
    v-progress-circular(v-if="loading" color="primary" indeterminate)
    nuxt-child(v-else :breadCrumbs="bc" :period="period")
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
      { title: 'Документ', to: 'dcis-periods-periodId-document', icon: 'file-table-box-multiple-outline' },
      { title: 'Атрибуты', to: 'dcis-periods-periodId-attributes', icon: 'file-table-box-multiple-outline' }
    ]))
    const { data: period, loading, update } = useCommonQuery<PeriodQuery, PeriodQueryVariables>({
      document: periodQuery,
      variables: () => ({
        periodId: route.params.periodId
      })
    })
    provide('periodUpdate', update)
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      if (loading.value) {
        return props.breadCrumbs
      }
      return [
        ...props.breadCrumbs,
        {
          text: period.value.project.name,
          to: localePath({ name: 'dcis-projects-projectId', params: { projectId: period.value.project.id } }),
          exact: true
        },
        { text: period.value.name, to: localePath({ name: 'dcis-periods-periodId' }), exact: true },
      ]
    })
    return { bc, drawer, links, period, loading }
  }
})
</script>
