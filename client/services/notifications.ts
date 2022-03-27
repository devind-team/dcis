import { NotificationsQuery, NotificationTypeEdge } from '~/types/graphql'
import { NotificationSubscriptionResultType } from '~/components/global/Notification.vue'

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
