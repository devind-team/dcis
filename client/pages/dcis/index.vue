<template lang="pug">
v-progress-circular(indeterminate color="primary")
</template>

<script lang="ts">
import { defineComponent } from '#app'
import { useRouter } from '#imports'
import { useI18n } from '~/composables'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const router = useRouter()
    const { localePath } = useI18n()
    router.push(localePath({ name: 'dcis-projects' }))
  }
})
</script>
