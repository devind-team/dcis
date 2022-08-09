<template lang="pug">
div
  left-navigator-driver(v-model="active" :items="links")
  nuxt-child(@update-drawer="active = !active" :key="$route.fullPath" :breadCrumbs="bc")
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
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.ac.names') as string })

    const active: Ref<boolean> = ref<boolean>(false)

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('panel.index') as string, to: localePath({ name: 'panel' }), exact: true },
      { text: t('panel.ac.name') as string, to: localePath({ name: 'panel-ac' }), exact: true }
    ]))

    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      {
        title: t('panel.ac.permissions.name') as string,
        to: 'panel-ac-permissions',
        permissions: 'auth.view_permission',
        icon: 'human'
      },
      {
        title: t('profile.activity.name') as string,
        to: 'panel-ac-activity',
        permissions: 'devind_core.view_logentry',
        icon: 'notebook-outline'
      },
      {
        title: t('profile.history.name') as string,
        to: 'panel-ac-history',
        permissions: 'devind_core.view_logrequest',
        icon: 'history'
      }
    ]))
    return { active, bc, links }
  }
})
</script>
