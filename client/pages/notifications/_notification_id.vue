<template lang="pug">
  bread-crumbs(:items="bc")
    v-row(v-if="!$apollo.queries.notification.loading")
      v-col.mx-auto(md="8")
        notification-page-view(
          v-if="kindView[notification.notice.kind] === 'page'"
          :page="notification.notice.page"
        )
        notification-mailing-view(
          v-else-if="kindView[notification.notice.kind] === 'mailing'"
          :mailing="notification.notice.mailing"
        )
    v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { AsyncComponent, PropType } from 'vue'
import { MetaInfo } from 'vue-meta'
import { mapGetters } from 'vuex'
import { defineComponent } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { notificationKinkView } from '~/components/notifications/NotificationsView.vue'

const NotificationPageView: AsyncComponent = () =>
  import('~/components/notifications/views/NotificationPageView.vue')
const NotificationMailingView: AsyncComponent = () =>
  import('~/components/notifications/views/NotificationMailingView.vue')

export default defineComponent({
  components: { BreadCrumbs, NotificationPageView, NotificationMailingView },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  head (): MetaInfo {
    return { title: this.$t('notifications.name') as string } as MetaInfo
  },
  computed: {
    ...mapGetters({ user: 'auth/user' }),
    bc (): BreadCrumbsItem[] {
      const bc: BreadCrumbsItem[] = [...this.breadCrumbs]
      if (!this.$apollo.queries.notification.loading) {
        bc.push({
          text: this.notification!.notice?.payload || 'Уведомление удалено',
          to: this.localePath({
            name: 'notifications-notification_id',
            params: { notification_id: this.notification!.id }
          }),
          exact: true
        })
      }
      return bc
    },
    kindView (): { [k: number]: string } {
      return notificationKinkView
    }
  },
  apollo: {
    notification: {
      query: require('~/gql/notifications/queries/notification.graphql'),
      variables () {
        return { notificationId: this.$route.params.notification_id }
      }
    }
  }
})
</script>
