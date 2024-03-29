<template lang="pug">
div
  left-navigator-driver(v-model="drawer" :items="links")
  v-progress-circular(v-if="periodLoading" color="primary" indeterminate)
  nuxt-child(v-else :bread-crumbs="bc" :period="archivePeriod" @update-drawer="drawer = !drawer")
</template>

<script lang="ts">
import { computed, defineComponent, inject, onUnmounted, PropType, ref, useRoute } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { usePeriodQuery } from '~/services/grapqhl/queries/dcis/periods'

export default defineComponent({
  components: { LeftNavigatorDriver, BreadCrumbs },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()

    const {
      data: archivePeriod,
      loading: periodLoading
    } = usePeriodQuery(route.params.archiveId)

    const drawer = ref<boolean>(false)
    const links = computed<LinksType[]>(() => [
      {
        title: t('dcis.periods.archive.document') as string,
        to: 'dcis-periods-archive-archiveId-document_sheets',
        query: { periodId: route.query.periodId as string },
        icon: 'file-table-box-multiple-outline'
      },
      {
        title: t('dcis.documents.links.attributes') as string,
        to: 'dcis-periods-archive-archiveId-attributes',
        query: { periodId: route.query.periodId as string },
        icon: 'page-next'
      },
      {
        title: t('dcis.periods.links.sheets') as string,
        to: 'dcis-periods-archive-archiveId-period_sheets',
        query: { periodId: route.query.periodId as string },
        icon: 'table'
      }
    ])

    const bc = computed<BreadCrumbsItem[]>(() => {
      if (periodLoading.value) {
        return props.breadCrumbs
      }
      return [
        ...props.breadCrumbs,
        {
          text: archivePeriod.value.name,
          to: localePath({ name: 'dcis-periods-periodId-documents', params: { periodId: route.query.periodId as string } }),
          exact: true
        },
        {
          text: t('dcis.periods.archive.name') as string,
          to: localePath({
            name: 'dcis-periods-archive-archiveId-document_sheets',
            query: route.query
          })
        }
      ]
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      route,
      archivePeriod,
      periodLoading,
      drawer,
      links,
      bc
    }
  }
})
</script>
