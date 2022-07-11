<template lang="pug">
v-progress-circular(color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent, useRouter } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  setup () {
    const router = useRouter()
    const { localePath } = useI18n()
    router.push(localePath({ name: 'profile-me' }))
  }
})
</script>
