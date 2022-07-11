<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')" fluid)
  template(#header) {{ $t('dashboard.general.name') }}
  .body-1 {{ $t('dashboard.general.activity') }}
  active-statistics
  .body-1 {{ $t('dashboard.general.clientDeviceStatistics') }}
  request-statistics
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import ActiveStatistics from '~/components/dashboard/general/ActiveStatistics.vue'
import RequestStatistics from '~/components/dashboard/general/RequestStatistics.vue'

export default defineComponent({
  components: { ActiveStatistics, RequestStatistics, LeftNavigatorContainer, BreadCrumbs },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    useNuxt2Meta({ title: t('dashboard.general.name') as string })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('dashboard.general.name') as string, to: localePath({ name: 'dashboard-general' }), exact: true }
    ]))
    return { bc }
  }
})
</script>
