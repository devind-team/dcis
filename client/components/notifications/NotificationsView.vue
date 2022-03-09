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
      v-list-item(@click="handleNotificationClick(mutate, notification).then()")
        v-list-item-avatar(v-if="notification.notice.user")
          avatar-dialog(:item="notification.notice.user")
        v-list-item-content(:class="{ 'text-gray-400': notification.hide }")
          v-list-item-title(v-html="t(kindView[notification.notice.kind], notification)" style="white-space: normal;")
          v-list-item-subtitle {{ $filters.dateTimeHM(notification.createdAt) }}
        v-list-item-icon.my-auto(v-if="!notification.read")
          v-icon(size="10" color="primary") mdi-circle
        v-list-item-action
          notification-menu(:notification="notification")
    v-list-item(v-if="notifications && notifications.length === 0")
      v-list-item-content
        v-alert(type="info") {{ $t('notifications.empty') }}
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { Component, Prop, Inject } from 'vue-property-decorator'
import { ApolloError } from 'apollo-client'
import { NotificationType } from '~/types/graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import NotificationMenu from '~/components/notifications/NotificationMenu.vue'

export const notificationKinkView: { [k: number]: string } = {
  0: 'info',
  1: 'page',
  2: 'comment',
  3: 'message',
  4: 'task',
  5: 'billing',
  6: 'paid',
  7: 'mailing',
  8: 'happyBirthday'
}

@Component<NotificationsView>({
  components: { NotificationMenu, AvatarDialog },
  computed: {
    kindView (): { [k: number]: string } {
      return notificationKinkView
    }
  }
})
export default class NotificationsView extends Vue {
  @Inject() setAlertApolloError!: (error: ApolloError) => void

  @Prop({ type: Array as PropType<NotificationType[]>, required: true }) notifications!: NotificationType[]

  readonly kindView!: { [k: number]: string }

  /**
   * Обработка нажатия на уведомление
   * @param mutate
   * @param notification
   */
  async handleNotificationClick (mutate: any, notification: NotificationType): Promise<void> {
    if (!notification.read) { await mutate() }
    await this.$router.push(this.localePath({
      name: 'notifications-notification_id',
      params: { notification_id: notification!.id }
    }))
    await this.$emit('open', notification)
  }

  /**
   * Получение перевода относительно локального пути
   * @param path
   * @param notification
   * @return
   */
  t (path: string, notification: NotificationType): string {
    const values = {
      user: notification.notice.user ? this.$getUserFullName(notification.notice.user) : '',
      payload: notification.notice.payload,
      objectId: notification.notice.objectId
    }
    return this.$t(`notifications.messages.${path}`, values) as string
  }
}
</script>
