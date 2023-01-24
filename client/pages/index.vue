<template lang="pug">
v-container
  v-progress-circular.mt-12.mx-auto(size="60" color="primary" indeterminate)
</template>

<script lang="ts">
import { useNuxt2Meta, defineComponent, onMounted, toRefs } from '#app'
import { useRouter } from '#imports'
import { useAuthStore } from '~/stores'
import { useI18n } from '~/composables'

export default defineComponent({
  setup () {
    const { t, localePath } = useI18n()
    const router = useRouter()
    const authStore = useAuthStore()

    useNuxt2Meta({ title: t('homePage') as string })

    onMounted(() => {
      const { loginIn } = toRefs(authStore)
      if (loginIn.value) {
        router.push(localePath({ name: 'dcis-projects' }))
      }
    })
  }
})
</script>
