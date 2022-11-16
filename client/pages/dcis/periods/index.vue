<template lang="pug">
v-row
  v-col.text-center
    v-progress-circular(color="primary" size="50" indeterminate)
</template>

<script lang="ts">
import { defineComponent } from '#app'
import { useRouter } from '#imports'
import { useI18n } from '~/composables'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { localePath } = useI18n()
    const router = useRouter()
    router.push(localePath({ name: 'dcis-projects' }))
  }
})
</script>
