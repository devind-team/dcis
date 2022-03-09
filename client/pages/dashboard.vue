<template lang="pug">
  div
    left-navigator-driver(v-model="drawer" :items="links")
    nuxt-child(:breadCrumbs="bc" @update-drawer="drawer = !drawer")
</template>

<script lang="ts">
import type { ComputedRef, Ref } from '#app'
import { computed, defineComponent, ref, useNuxt2Meta } from '#app'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useI18n } from '~/composables'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'

export default defineComponent({
  components: { LeftNavigatorDriver },
  middleware: 'auth',
  permissions: 'core.view_user',
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('dashboard.index') as string })

    const drawer: Ref<boolean> = ref<boolean>(false)

    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      { title: t('dashboard.general.name') as string, to: 'dashboard-general', icon: 'view-dashboard-outline' }
    ]))

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('dashboard.index') as string, to: localePath({ name: 'dashboard' }), exact: true }
    ]))
    return { drawer, links, bc }
  }
})
</script>
