<template lang="pug">
  v-card
    v-card-title {{ $t('profile.me.profile') }} {{ $getUserFullName(user) }}
    v-card-subtitle {{ $t('profile.me.registrationDate') }} {{ date(user.createdAt) }}
    v-card-text
      v-row
        v-col(cols="12" md="3") {{ $t('profile.me.userAvatar') }}
        v-col(cols="12" md="9")
          avatar-view(:user="user")
      basic-information(:user="user")
      additional-information(:viewUser="user")
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, toRef, useNuxt2Meta } from '#app'
import type { UserType } from '~/types/graphql'
import { useFilters, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import AvatarView from '~/components/users/AvatarView.vue'
import BasicInformation from '~/components/profile/BasicInformation.vue'
import AdditionalInformation from '~/components/profile/AdditionalInformation.vue'

export default defineComponent({
  components: { AdditionalInformation, BasicInformation, AvatarView },
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
