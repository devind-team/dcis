<template lang="pug">
  v-list(two-line)
    apollo-mutation(
      v-for="notification in notifications"
      v-slot="{ mutate }"
      :key="notification.id"
      :mutation="require('~/gql/notifications/mutations/change_notification.graphql')"
      :variables="{ notificationId: notification.id, field: 'read', value: true }"
      @error="setAlertApolloError"
      tag
    )
      v-list-item(@click="handleNotificationClick(mutate, notification)")
        v-list-item-avatar(v-if="notification.notice.user")
          avatar-dialog(:item="notification.notice.user")
        v-list-item-content(:class="{ 'text-gray-400': notification.hide }")
          v-list-item-title(v-html="tl(notificationKinkView[notification.notice.kind], notification)" style="white-space: normal;")
          v-list-item-subtitle {{ dateTimeHM(notification.createdAt) }}
        v-list-item-icon.my-auto(v-if="!notification.read")
          v-icon(size="10" color="primary") mdi-circle
        v-list-item-action
          notification-menu(:notification="notification")
    v-list-item(v-if="notifications && notifications.length === 0")
      v-list-item-content
        v-alert(type="info") {{ $t('notifications.empty') }}
</template>

<script lang="ts">
import { ApolloError } from 'apollo-client'
import type { PropType } from '#app'
import { defineComponent, inject, useRouter } from '#app'
import { useConvertors, useFilters, useI18n } from '~/composables'
import { NotificationType } from '~/types/graphql'
import { notificationKinkView } from '~/services/notifications'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import NotificationMenu from '~/components/notifications/NotificationMenu.vue'

export default defineComponent({
  components: { NotificationMenu, AvatarDialog },
  props: {
    notifications: { type: Array as PropType<NotificationType[]>, required: true }
  },
  setup (_, { emit }) {
    const router = useRouter()
    const { t, localePath } = useI18n()
    const { dateTimeHM } = useFilters()
    const { getUserFullName } = useConvertors()

    const setAlertApolloError: (error: ApolloError) => void = inject('setAlertApolloError')

    const handleNotificationClick = (mutate: any, notification: NotificationType) => {
      if (!notification.read) { mutate() }
      router.push(localePath({
        name: 'notifications-notificationId',
        params: { notificationId: notification!.id }
      }))
      emit('open', notification)
    }

    const tl = (path: string, notification: NotificationType): string => {
      const values = {
        user: notification.notice.user ? getUserFullName(notification.notice.user) : '',
        payload: notification.notice.payload,
        objectId: notification.notice.objectId
      }
      return t(`notifications.messages.${path}`, values) as string
    }

    return { setAlertApolloError, notificationKinkView, handleNotificationClick, tl, dateTimeHM }
  }
})
</script>
