<template lang="pug">
v-card
  v-card-title {{ $t('profile.me.profile') }} {{ $getUserFullName(user) }}
  v-card-text
    basic-information(:user="user")
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, toRef, useNuxt2Meta } from '#app'
import type { UserType } from '~/types/graphql'
import { useFilters, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import BasicInformation from '~/components/profile/BasicInformation.vue'

export default defineComponent({
  components: { BasicInformation },
  middleware: 'auth',
  setup () {
    const userStore = useAuthStore()
    const { date } = useFilters()
    const { t } = useI18n()
    useNuxt2Meta({ title: t('profile.me.myProfile') as string })
    const user: Ref<UserType> = toRef(userStore, 'user')
    return { date, user }
  }
})
</script>
