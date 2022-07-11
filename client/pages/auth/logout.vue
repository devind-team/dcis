<template lang="pug">
v-container
  v-row
    v-col
      v-progress-linear(indeterminate)
      v-alert(type="info" text) {{ $t('auth.logout.loggingOut') }}
</template>

<script lang="ts">
import { defineComponent, useNuxt2Meta, useRouter } from '#app'
import { useApolloHelpers, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const router = useRouter()
    const { t, localePath } = useI18n()
    const { onLogout, defaultClient } = useApolloHelpers()
    const userStore = useAuthStore()

    useNuxt2Meta({ title: t('auth.logout.logout') as string })

    if (userStore.loginIn) {
      userStore.logout()
      onLogout(defaultClient, true)
    }
    // Необходимо для нормальной перезагрузки сокетов
    router.push(localePath({ name: 'index' }))
  }
})
</script>
