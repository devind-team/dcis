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
          v-list-item-content {{ t(`${notification.read ? 'markAsUnread' : 'markAsRead'}`) }}
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
          v-list-item-content {{ t(`${notification.hide ? 'restore' : 'delete'}`) }}
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
          v-list-item-content {{ t('deleteAllForEveryone') }}
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { Component, Prop, Inject } from 'vue-property-decorator'
import { ApolloError } from 'apollo-client'
import { mapGetters } from 'vuex'
import { NotificationType } from '~/types/graphql'

@Component<NotificationMenu>({
  computed: mapGetters({ hasPerm: 'auth/hasPerm' })
})
export default class NotificationMenu extends Vue {
  @Inject() setAlertApolloError!: (error: ApolloError) => void

  @Prop({ type: Object as PropType<NotificationType>, required: true }) notification!: NotificationType

  readonly hasPerm!: (permissions: string | string[], or?: boolean) => boolean

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`notifications.${path}`, values) as string
  }
}
</script>
