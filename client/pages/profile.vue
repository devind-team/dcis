<template lang="pug">
bread-crumbs(:items="bc")
  two-columns(:links="links")
    nuxt-child
</template>

<script lang="ts">
import type { ComputedRef } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import TwoColumns from '~/components/common/grid/TwoColumns.vue'

export default defineComponent({
  components: { TwoColumns, BreadCrumbs },
  middleware: 'auth',
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('profile.userProfile') as string })

    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      { title: t('profile.me.profile') as string, to: 'profile-me', icon: 'face-man' },
      { title: t('profile.settings.index') as string, to: 'profile-settings', icon: 'cogs' },
      { title: t('profile.security.name') as string, to: 'profile-security', icon: 'security' },
      { title: t('profile.file') as string, to: 'profile-files', icon: 'file-multiple' },
      {
        title: t('profile.activity.name') as string,
        to: 'profile-activity',
        permissions: 'devind_core.view_logentry',
        icon: 'notebook-outline'
      },
      {
        title: t('profile.history.name') as string,
        to: 'profile-history',
        permissions: 'devind_core.view_logrequest',
        icon: 'history'
      }
    ]))

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('profile.userProfile') as string, to: localePath({ name: 'profile-me' }), exact: true }
    ]))
    return { links, bc }
  }
})
</script>
