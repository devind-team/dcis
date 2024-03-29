<template lang="pug">
bread-crumbs(:items="bc")
  v-row(v-if="!loading")
    v-col.mx-auto(md="8")
      notification-mailing-view(
        v-if="notificationKinkView[notification.notice.kind] === 'mailing'"
        :mailing="notification.notice.mailing"
      )
  v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { defineComponent, useNuxt2Meta, computed } from '#app'
import { useRoute } from '#imports'
import { useCommonQuery, useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { NotificationQuery, NotificationQueryVariables } from '~/types/graphql'
import { notificationKinkView } from '~/services/notifications'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import NotificationMailingView from '~/components/notifications/views/NotificationMailingView.vue'
import notificationQuery from '~/gql/notifications/queries/notification.graphql'

export default defineComponent({
  components: { BreadCrumbs, NotificationMailingView },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const route = useRoute()
    const { t, localePath } = useI18n()

    useNuxt2Meta({ title: t('notifications.name') as string })

    const { data: notification, loading } = useCommonQuery<NotificationQuery, NotificationQueryVariables>({
      document: notificationQuery,
      variables: () => ({ notificationId: route.params.notificationId })
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      const crumbs: BreadCrumbsItem[] = [...props.breadCrumbs]
      if (!loading.value) {
        crumbs.push({
          text: notification.value.notice.payload,
          to: localePath({
            name: 'notifications-notificationId',
            params: { notificationId: notification.value.id }
          }),
          exact: true
        })
      }
      return crumbs
    })

    return { bc, notification, loading, notificationKinkView }
  }
})
</script>
