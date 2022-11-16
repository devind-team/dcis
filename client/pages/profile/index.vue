<template lang="pug">
v-progress-circular(color="primary" indeterminate)
</template>

<script lang="ts">
import { defineComponent } from '#app'
import { useRouter } from '#imports'
import { useI18n } from '~/composables'

export default defineComponent({
  setup () {
    const router = useRouter()
    const { localePath } = useI18n()
    router.push(localePath({ name: 'profile-me' }))
  }
})
</script>
