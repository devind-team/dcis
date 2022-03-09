<template lang="pug">
  v-menu(transition="slide-y-transition" left)
    template(#activator="{ on, attrs }")
      v-btn(v-on="on" v-bind="attrs" icon)
        v-icon mdi-dots-horizontal
    v-list
      apollo-mutation(
        v-if="notifications.length"
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
            v-list-item-title {{ t('markAsReadAll') }}
      apollo-mutation(
        v-if="notifications.length"
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
            v-list-item-title {{ t('deleteAll') }}
      v-list-item(:to="localePath('profile-settings')")
        v-list-item-icon
          v-icon mdi-cog
        v-list-item-content
          v-list-item-title {{ t('settings') }}
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { Component, Inject, Prop } from 'vue-property-decorator'
import { ApolloError } from 'apollo-client'
import { NotificationType } from '~/types/graphql'

@Component<NotificationsMenu>({})
export default class NotificationsMenu extends Vue {
  @Inject() setAlertApolloError!: (error: ApolloError) => void

  @Prop({ type: Array as PropType<NotificationType[]>, required: true }) notifications!: NotificationType[]

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
