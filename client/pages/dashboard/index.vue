<template lang="pug">
  v-progress-circular(color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, useRouter } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { localePath } = useI18n()
    const router = useRouter()
    router.push(localePath({ name: 'dashboard-general' }))
  }
})
</script>
