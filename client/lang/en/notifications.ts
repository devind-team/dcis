export default {
  name: 'Notifications',
  all: 'See all',
  settings: 'Notification settings',
  empty: 'No new notifications',
  markAsRead: 'Mark as read',
  markAsReadAll: 'Mark all as read',
  markAsUnread: 'Mark as unread',
  restore: 'Restore notification',
  delete: 'Delete notification',
  deleteAll: 'Delete all notifications',
  deleteAllForEveryone: 'Delete notification for everyone',
  messages: {
    info: 'System message',
    page: 'The user <strong>{user}</strong> added a new page <strong>{payload}</strong>.',
    comment: 'The user <strong>{user}</strong> added a new comment to your post.',
    message: 'The user <strong>{user}</strong> sent you a new message.',
    task: 'The task completed.',
    billing: 'The user <strong>{user}</strong> issued an invoice for payment.',
    paid: 'The invoice #<strong>{objectId}</strong> paid successfully.',
    mailing: 'Received a notification <strong>{payload}</strong>.&#9993;',
    happyBirthday: 'Happy birthday to you!'
  }
}
