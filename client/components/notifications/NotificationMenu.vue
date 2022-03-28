<template lang="pug">
  v-menu(transition="slide-y-transition" bottom)
    template(#activator="{ on, attrs }")
      v-btn(v-on="on" v-bind="attrs" icon)
        v-icon mdi-dots-horizontal
    v-list
      apollo-mutation(
        v-slot="{ mutate }"
        :mutation="require('~/gql/notifications/mutations/change_notification.graphql')"
        :variables="{ notificationId: notification.id, field: 'read', value: !notification.read }"
        @error="setAlertApolloError"
        tag
      )
        v-list-item(@click="mutate")
          v-list-item-icon
            v-icon mdi-check
          v-list-item-content {{ $t(`notifications.${notification.read ? 'markAsUnread' : 'markAsRead'}`) }}
      apollo-mutation(
        v-slot="{ mutate }"
        :mutation="require('~/gql/notifications/mutations/change_notification.graphql')"
        :variables="{ notificationId: notification.id, field: 'hide', value: !notification.hide }"
        @error="setAlertApolloError"
        tag
      )
        v-list-item(@click="mutate")
          v-list-item-icon
            v-icon mdi-close-circle-outline
          v-list-item-content {{ $t(`notifications.${notification.hide ? 'restore' : 'delete'}`) }}
      apollo-mutation(
        v-slot="{ mutate }"
        :mutation="require('~/gql/notifications/mutations/delete_notice.graphql')"
        :variables="{ noticeId: notification.notice.id }"
        @error="setAlertApolloError"
        tag
      )
        v-list-item(v-if="hasPerm('notifications.delete_notice')" @click="mutate")
          v-list-item-icon
            v-icon mdi-close-circle-multiple-outline
          v-list-item-content {{ $t('notifications.deleteAllForEveryone') }}
</template>

<script lang="ts">
import { ApolloError } from 'apollo-client'
import type { PropType, Ref } from '#app'
import { defineComponent, inject, toRef } from '#app'
import { NotificationType } from '~/types/graphql'
import { HasPermissionFnType, useAuthStore } from '~/store'

export default defineComponent({
  props: {
    notification: { type: Object as PropType<NotificationType>, required: true }
  },
  setup () {
    const authStore = useAuthStore()
    const hasPerm: Ref<HasPermissionFnType> = toRef(authStore, 'hasPerm')
    const setAlertApolloError: (error: ApolloError) => void = inject('setAlertApolloError')
    return { setAlertApolloError, hasPerm }
  }
})
</script>
