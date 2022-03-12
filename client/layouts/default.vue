<template lang="pug">
  v-app
    navigation(v-model="drawer")
    app-bar(v-model="drawer")
    v-main
      nuxt
    footer-component(v-if="footer")
</template>

<script lang="ts">
import { Vue, Component, Provide } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import notificationsQuery from '~/gql/notifications/queries/notifications.graphql'
import { NotificationsQuery, NotificationType, NotificationTypeEdge, PageInfo, UserType } from '~/types/graphql'
import Navigation from '~/components/global/Navigation.vue'
import AppBar from '~/components/global/AppBar.vue'
import FooterComponent from '~/components/global/FooterComponent.vue'
import { updateQueryNotifications } from '~/components/global/Notification.vue'

@Component<DefaultLayout>({
  components: { AppBar, Navigation, FooterComponent },
  computed: mapGetters({ user: 'auth/user', loginIn: 'auth/loginIn' }),
  watch: {
    '$colorMode.value': {
      handler () {
        this.$vuetify.theme.dark = this.$colorMode.value === 'dark'
      },
      immediate: true
    }
  },
  apollo: {
    notifications: {
      query: notificationsQuery,
      variables () { return { userId: this.user.id, first: this.notificationPageSize } },
      update ({ notifications }: NotificationsQuery | any): NotificationType[] {
        this.notificationPageInfo = notifications.pageInfo
        return notifications.edges.map((e: NotificationTypeEdge) => e.node) as NotificationType[]
      },
      subscribeToMore: {
        document: require('~/gql/notifications/subscriptions/notifications.graphql'),
        updateQuery: updateQueryNotifications
      },
      loadingKey: 'notificationLoading',
      skip () {
        return !this.loginIn
      }
    }
  }
})
export default class DefaultLayout extends Vue {
  @Provide() layoutInstance: DefaultLayout = this
  readonly loginIn!: boolean
  readonly user!: UserType
  readonly notifications!: NotificationType[] | undefined

  public footer: boolean = true
  drawer: boolean = false

  notificationLoading: boolean = false
  notificationPageSize: number = 25
  notificationPageInfo: PageInfo = { hasNextPage: true, hasPreviousPage: true }

  setFooter (state: boolean = true) {
    this.footer = state
  }
}
</script>
