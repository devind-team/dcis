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
    const { localePath } = useI18n()

    const breadCrumbs: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: 'Проекты сборов', to: localePath({ name: 'dcis-documents' }), exact: true }
    ]))
    return { breadCrumbs }
  }
})
</script>
