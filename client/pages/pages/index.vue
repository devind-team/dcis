<template lang="pug">
  bread-crumbs(:items="bc" fluid)
    .text-h4.text-md-h2.mb-7 {{ $t('pages.newsFeed') }}
    page-grid(:pages="[]" allow-loading)
</template>

<script lang="ts">
import type { ComputedRef } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import PageGrid from '~/components/pages/views/PageGrid.vue'

export default defineComponent({
  components: { PageGrid, BreadCrumbs },
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('pages.index') as string })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('index.main') as string, to: localePath({ name: 'index' }), exact: true },
      { text: t('pages.index') as string, to: localePath({ name: 'pages' }), exact: true }
    ]))
    return { bc }
  }
})
</script>
