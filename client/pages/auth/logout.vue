<template lang="pug">
  v-container
    v-row
      v-col
        v-progress-linear(indeterminate)
        v-alert(type="info" text) {{ $t('auth.logout.loggingOut') }}
</template>

<script lang="ts">
import { defineComponent, useNuxt2Meta, useNuxtApp } from '#app'
import { useApolloHelpers, useI18n } from '~/composables'
import { useAuthStore } from '~/store/auth-store'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { t, localePath } = useI18n()
    const { onLogout, defaultClient } = useApolloHelpers()
    const { $store } = useNuxtApp()
    const userStore = useAuthStore()

    useNuxt2Meta({ title: t('auth.logout.logout') as string })

    if (userStore.loginIn) {
      userStore.logout()
      // Убрать после удаления vuex
      $store.dispatch('auth/logout')
      onLogout(defaultClient)
    }
    // Необходимо для нормальной перезагрузки сокетов
    if (process.client) {
      window.location.href = localePath({ name: 'index' })
    }
  }
})
</script>
