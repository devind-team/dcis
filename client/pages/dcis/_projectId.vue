<template lang="pug">
  div
    left-navigator-driver(v-model="drawer" :items="links")
    nuxt-child
</template>

<script lang="ts">
import type { Ref, ComputedRef } from '#app'
import { computed, defineComponent, ref } from '#app'
import { LinksType } from '~/types/devind'
import LeftNavigatorDriver from '~/components/common/grid/LeftNavigatorDriver.vue'

export default defineComponent({
  components: { LeftNavigatorDriver },
  middleware: 'auth',
  setup () {
    const drawer: Ref<boolean> = ref<boolean>(false)
    const links: ComputedRef<LinksType[]> = computed<LinksType[]>(() => ([
      { title: 'Сбор', to: 'dcis-projectId-collection', icon: 'file-table-box-multiple-outline' },
      { title: 'Пользователи', to: 'dcis-projectId-accounts', icon: 'account-wrench' },
      { title: 'Настройки', to: 'dcis-projectId-settings', icon: 'cogs' }
    ]))
    return { drawer, links }
  }
})
</script>
