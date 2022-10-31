<template lang="pug">
v-progress-circular(indeterminate color="primary")
</template>

<script lang="ts">
import { defineComponent, useRouter } from '#app'
import { useI18n } from '~/composables'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const router = useRouter()
    const { localePath } = useI18n()
    router.push(localePath({ name: 'dcis-dictionaries-privileges' }))
  }
})
</script>
