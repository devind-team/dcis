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
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.dictionaries') as string })

    const drawer: Ref<boolean> = ref<boolean>(false)

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('panel.index') as string, to: localePath({ name: 'panel' }), exact: true },
      { text: t('panel.dictionaries') as string, to: localePath({ name: 'panel-dictionaries' }), exact: true }
    ]))

    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      { title: 'Профиль', to: 'panel-dictionaries-profile', permissions: 'core.view_user', icon: 'passport' }
    ]))

    return { drawer, bc, links }
  }
})
</script>
