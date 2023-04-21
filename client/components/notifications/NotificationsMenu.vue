<template lang="pug">
v-menu(transition="slide-y-transition" left)
  template(#activator="{ on, attrs }")
    v-btn(v-on="on" v-bind="attrs" icon)
      v-icon mdi-dots-horizontal
  v-list
    apollo-mutation(
      v-slot="{ mutate }"
      @error="setAlertApolloError"
      :mutation="require('~/gql/notifications/mutations/change_notifications.graphql')"
      :variables="{ notificationsId: notifications.filter(e => !e.read).map(e => e.id), field: 'read', value: true }"
      tag
    )
      v-list-item(@click="mutate")
        v-list-item-icon
          v-icon mdi-check
        v-list-item-content
          v-list-item-title {{ $t('notifications.markAsReadAll') }}
    apollo-mutation(
      v-slot="{ mutate }"
      @error="setAlertApolloError"
      :mutation="require('~/gql/notifications/mutations/change_notifications.graphql')"
      :variables="{ notificationsId: notifications.filter(e => !e.hide).map(e => e.id), field: 'hide', value: true }"
      tag
    )
      v-list-item(@click="mutate")
        v-list-item-icon
          v-icon mdi-close-circle-multiple-outline
        v-list-item-content
          v-list-item-title {{ $t('notifications.deleteAll') }}
</template>

<script lang="ts">
import { ApolloError } from 'apollo-client'
import type { PropType } from '#app'
import { defineComponent, inject } from '#app'
import { NotificationType } from '~/types/graphql'

export default defineComponent({
  props: {
    notifications: { type: Array as PropType<NotificationType[]>, required: true }
  },
  setup () {
    const setAlertApolloError: (error: ApolloError) => void = inject('setAlertApolloError')
    return { setAlertApolloError }
  }
})
</script>
