<template lang="pug">
  nuxt-child(:breadCrumbs="bc" :key="this.$route.params.notification_id || 'index'")
</template>

<script lang="ts">
import type { ComputedRef } from '#app'
import { computed, defineComponent } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { t, localePath } = useI18n()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('notifications.name') as string, to: localePath({ name: 'notifications' }), exact: true }
    ]))
    return { bc }
  }
})

</script>
