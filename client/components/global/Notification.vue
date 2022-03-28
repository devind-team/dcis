<template lang="pug">
  v-menu(v-model="menu" :close-on-content-click="false" bottom)
    template(#activator="{ on }")
      v-btn.mr-5(v-on="on" icon text)
        v-badge(:value="newNotificationsLength" :content="newNotificationsLength" overlap)
          v-icon mdi-bell
    v-card(max-width="600" min-width="500")
      v-card-title {{ $t('notifications.name') }}
        v-spacer
        nuxt-link.caption(:to="localePath({ name: 'notifications' })" @click.native="menu = false")
          | {{ $t('notifications.all') }}
      v-card-text(style="max-height: 500px; overflow-y: auto")
        mutation-result-alert(ref="mutationResultAlert")
        notifications-view(:notifications="notifications" @open="menu = false")
</template>

<script lang="ts">
import { ApolloError } from 'apollo-client'
import type { Ref, ComputedRef } from '#app'
import { defineComponent, inject, provide, ref, computed } from '#app'
import { NotificationsSubscription, NotificationType } from '~/types/graphql'
import MutationResultAlert from '~/components/common/MutationResultAlert.vue'
import NotificationsView from '~/components/notifications/NotificationsView.vue'

export type NotificationSubscriptionResultType = { subscriptionData: { data: { notifications: NotificationsSubscription } } }

export default defineComponent({
  components: { MutationResultAlert, NotificationsView },
  setup () {
    const menu: Ref<boolean> = ref<boolean>(false)
    const mutationResultAlert = ref<InstanceType<typeof MutationResultAlert> | null>(null)
    const notifications: ComputedRef<NotificationType[]> = inject<ComputedRef<NotificationType[]>>('notifications')

    const newNotificationsLength: ComputedRef<number> = computed<number>(() => (
      notifications.value ? notifications.value.filter((e: NotificationType) => !e.read).length : 0
    ))
    const setApolloError = (error: ApolloError): void => {
      mutationResultAlert.value.setApolloError(error)
    }
    provide<(error: ApolloError) => void>('setAlertApolloError', setApolloError)
    return { menu, notifications, newNotificationsLength, mutationResultAlert }
  }
})
</script>
