<template lang="pug">
  v-app
    navigation(v-model="drawer")
    app-bar(v-model="drawer")
    v-main
      nuxt
    footer-component(v-if="footer")
</template>

<script lang="ts">
import type { Ref, ComputedRef } from '#app'
import { defineComponent, provide, ref, toRefs, watchEffect } from '#app'
import { useAuthStore } from '~/stores'
import { useCursorPagination, useQueryRelay, useVuetify } from '~/composables'
import { updateQueryNotifications } from '~/services/notifications'
import { NotificationsQuery, NotificationsQueryVariables, NotificationType, UserType } from '~/types/graphql'
import notificationsSubscription from '~/gql/notifications/subscriptions/notifications.graphql'
import notificationsQuery from '~/gql/notifications/queries/notifications.graphql'
import AppBar from '~/components/global/AppBar.vue'
import Navigation from '~/components/global/Navigation.vue'
import FooterComponent from '~/components/global/FooterComponent.vue'

export default defineComponent({
  components: { AppBar, Navigation, FooterComponent },
  setup () {
    const authStore = useAuthStore()
    const { vuetify, isDark } = useVuetify()

    const { user, loginIn } = toRefs<{ user: UserType, loginIn: boolean }>(authStore)

    const drawer = ref<boolean>(false)
    const footer = ref<boolean>(true)

    const {
      data: notifications,
      loading: notificationLoading,
      subscribeToMore
    } = useQueryRelay<NotificationsQuery, NotificationsQueryVariables, NotificationType>({
      document: notificationsQuery,
      variables: () => ({ userId: user.value?.id }),
      options: () => ({
        enabled: loginIn.value
      })
    }, {
      pagination: useCursorPagination()
    })

    subscribeToMore({
      document: notificationsSubscription,
      updateQuery: updateQueryNotifications,
      onError () {
        typeof window !== 'undefined' && window.location.reload()
      }
    })

    watchEffect(() => {
      vuetify.theme.dark = isDark.value
    })

    const setFooter = (state: boolean = true): void => {
      footer.value = state
    }

    provide<ComputedRef<NotificationType[]>>('notifications', notifications)
    provide<Ref<boolean>>('notificationLoading', notificationLoading)
    provide<(state: boolean) => void>('setFooter', setFooter)
    return { drawer, footer }
  }
})
</script>
