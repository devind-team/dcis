<template lang="pug">
div
  left-navigator-driver(v-model="active" :items="links")
  nuxt-child(:breadCrumbs="bc" @update-drawer="active = !active")
</template>

<script lang="ts">
import type { ComputedRef, Ref } from '#app'
import { defineComponent, computed, useNuxt2Meta, ref } from '#app'
import { BreadCrumbsItem, LinksType } from '~/types/devind'
import { useI18n } from '~/composables'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'
export default defineComponent({
  components: { LeftNavigatorDriver },
  middleware: ['auth'],
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('dictionaries.name') as string })
    const active: Ref<boolean> = ref<boolean>(false)
    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      {
        title: t('dictionaries.privileges.header') as string,
        to: 'dcis-dictionaries-privileges',
        icon: 'human-queue'
      },
      {
        title: t('dictionaries.organizations.header') as string,
        to: 'dcis-dictionaries-organizations',
        icon: 'home-city'
      },
      {
        title: t('dictionaries.departments.header') as string,
        to: 'dcis-dictionaries-departments',
        icon: 'briefcase'
      },
      {
        title: t('dictionaries.budgetClassifications.header') as string,
        to: 'dcis-dictionaries-budget_classifications',
        icon: 'cash-multiple'
      },
      {
        title: t('dictionaries.statuses.header') as string,
        to: 'dcis-dictionaries-statuses',
        icon: 'list-status'
      },
      {
        title: t('dictionaries.addStatuses.header') as string,
        to: 'dcis-dictionaries-add_statuses',
        icon: 'check-all'
      }
    ]))
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('dictionaries.dcis') as string, to: localePath({ name: 'dcis' }), exact: true }
    ]))
    return { active, bc, links }
  }
})
</script>
