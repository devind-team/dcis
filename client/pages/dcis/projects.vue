<template lang="pug">
  nuxt-child(:breadCrumbs="breadCrumbs")
</template>

<script lang="ts">
import type { ComputedRef } from '#app'
import { computed, defineComponent } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { t, localePath } = useI18n()

    const breadCrumbs: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('dcis.home') as string, to: localePath({ name: 'dcis-projects' }), exact: true }
    ]))
    return { breadCrumbs }
  }
})
</script>
