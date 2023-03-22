<template lang="pug">
  v-row
    v-col.text-center
      v-progress-circular(color="primary" size="50" indeterminate)
</template>

<script lang="ts">
import { defineComponent, useRoute, useRouter } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { localePath } = useI18n()
    const router = useRouter()
    const route = useRoute()
    router.push(localePath({ name: 'dcis-periods-archive-archiveId-period_sheets', query: route.query }))
  }
})
</script>
