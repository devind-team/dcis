<template lang="pug">
bread-crumbs(:items="bc" fluid)
  cards-navigator(:items="cards")
</template>

<script lang="ts">
import type { ComputedRef } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import CardsNavigator from '~/components/common/grid/CardsNavigator.vue'

export default defineComponent({
  components: { CardsNavigator, BreadCrumbs },
  middleware: 'auth',
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.index') as string })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('panel.index') as string, to: localePath({ name: 'panel' }), exact: true }
    ]))

    const cards: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      {
        title: t('panel.ac.name') as string,
        icon: 'mdi-account',
        permissions: [
          'core.view_user',
          'auth.view_group',
          'dcis.view_curatorgroup',
          'auth.view_permission',
          'devind_core.view_logentry',
          'devind_core.view_logrequest'
        ],
        permOr: true,
        to: localePath({ name: 'panel-ac' }),
        color: 'info'
      },
      {
        title: t('panel.support') as string,
        icon: 'mdi-face-agent',
        to: localePath({ name: 'panel-support' }),
        color: 'success'
      },
      {
        title: t('panel.dictionaries') as string,
        icon: 'mdi-book-alphabet',
        to: localePath({ name: 'panel-dictionaries' }),
        color: 'brown'
      }
    ]))

    return { bc, cards }
  }
})
</script>
