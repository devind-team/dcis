<template lang="pug">
v-container
  v-row
    v-col
      v-progress-linear(indeterminate)
      v-alert(type="info" text) {{ $t('auth.logout.loggingOut') }}
</template>

<script lang="ts">
import { defineComponent, toRefs, useNuxt2Meta } from '#app'
import { useRouter } from '#imports'
import { useApolloHelpers, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const router = useRouter()
    const { t, localePath } = useI18n()
    const { onLogout, defaultClient } = useApolloHelpers()
    const authStore = useAuthStore()
    const { loginIn } = toRefs(authStore)
    useNuxt2Meta({ title: t('auth.logout.logout') as string })

    if (loginIn.value) {
      authStore.logout()
      setTimeout(() => {
        onLogout(defaultClient, true)
      }, 0)
    }
    // Необходимо для нормальной перезагрузки сокетов
    router.push(localePath({ name: 'index' }))
  }
})
</script>
