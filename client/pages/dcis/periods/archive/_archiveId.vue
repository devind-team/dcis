<template lang="pug">
div
  left-navigator-driver(v-model="drawer" :items="links")
  v-progress-circular(v-if="loading" color="primary" indeterminate)
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
      loading
    } = usePeriodQuery(route.params.archiveId)
    const drawer = ref<boolean>(false)
    const links = computed<LinksType[]>(() => {
      const result: LinksType[] = [
        {
          title: t('dcis.documents.links.sheets') as string,
          to: 'dcis-archive-archiveId-document_sheets',
          icon: 'file-table-box-multiple-outline'
        },
        {
          title: t('dcis.documents.links.attributes') as string,
          to: 'dcis-archive-archiveId-attributes',
          icon: 'page-next'
        },
        {
          title: t('dcis.periods.links.sheets') as string,
          to: 'dcis-archive-archiveId-period_sheets',
          icon: 'table'
        }
      ]
      return result
    })

    const bc = computed<BreadCrumbsItem[]>(() => {
      if (loading.value) {
        return props.breadCrumbs
      }
      return [
        ...props.breadCrumbs,
        { text: archivePeriod.value.name, to: localePath({ name: 'dcis-periods-periodId-documents' }), exact: true }
      ]
    })

    const setFooter = inject<(state: boolean) => void>('setFooter')
    setFooter(false)
    onUnmounted(() => {
      setFooter(true)
    })

    return {
      archivePeriod,
      loading,
      drawer,
      links,
      bc
    }
  }
})
</script>
