<template lang="pug">
  v-menu(v-model="menu" :close-on-content-click="false" bottom)
    template(#activator="{ on }")
      v-btn.mr-5(v-on="on" icon text)
        v-badge(:value="newNotificationsLength" :content="newNotificationsLength" overlap)
          v-icon mdi-bell
    v-card(max-width="600" min-width="500")
      v-card-title {{ t('name') }}
        v-spacer
        nuxt-link.caption(:to="localePath({ name: 'notifications' })" @click.native="menu = false") {{ t('all') }}
      v-card-text(style="max-height: 500px; overflow-y: auto")
        mutation-result-alert(ref="mutationResultAlert")
        notifications-view(:notifications="layoutInstance.notifications" @open="menu = false")
</template>

<script lang="ts">
import Vue, { AsyncComponent } from 'vue'
import { ApolloError } from 'apollo-client'
import { mapGetters } from 'vuex'
import {
  NotificationsQuery,
  NotificationType,
  NotificationTypeEdge,
  NotificationsSubscription
} from '~/types/graphql'
import MutationResultAlert from '~/components/common/MutationResultAlert.vue'

const NotificationsView: AsyncComponent = () => import('~/components/notifications/NotificationsView.vue')

export type NotificationSubscriptionResultType = { subscriptionData: { data: { notifications: NotificationsSubscription } } }

export const updateQueryNotifications = (
  previousResult: NotificationsQuery | any,
  { subscriptionData: { data: { notifications: { action, id, notification } } } }: NotificationSubscriptionResultType
) => {
  if (action === 'ADD') {
    previousResult.notifications.edges = [
      { node: notification, __typename: 'NotificationTypeEdge' },
      ...previousResult.notifications.edges
    ]
    ++previousResult.notifications.totalCount
  } else if (action === 'CHANGE') {
    const nodeNotification: NotificationTypeEdge | undefined = previousResult.notifications.edges
      .find((e: NotificationTypeEdge) => e.node!.id === notification!.id)
    if (nodeNotification) {
      nodeNotification!.node = notification
    }
  } else if (action === 'DELETE') {
    previousResult.notifications.edges = previousResult.notifications
      .edges.filter((e: NotificationTypeEdge) => e.node?.id !== id)
    --previousResult.notifications.totalCount
  }
  return previousResult
}

export default Vue.extend<any, any, any, any>({
  components: { MutationResultAlert, NotificationsView },
  inject: ['layoutInstance'],
  provide () {
    return {
      setAlertApolloError: this.setApolloError
    }
  },
  data: () => ({
    menu: false
  }),
  computed: {
    ...mapGetters({ user: 'auth/user' }),
    newNotificationsLength (): number {
      return this.layoutInstance.notifications ? this.layoutInstance.notifications.filter((e: NotificationType) => !e.read).length : 0
    }
  },
  methods: {
    /**
     * Получение перевода относильно локального пути
     * @param path
     * @param values
     * @return
     */
    t (path: string, values: any = undefined): string {
      return this.$t(`notifications.${path}`, values) as string
    },
    /**
     * Установка ошибки Apollo
     * @param error
     */
    setApolloError (error: ApolloError): void {
      this.$refs.mutationResultAlert.setApolloError(error)
    }
  }
})
</script>
