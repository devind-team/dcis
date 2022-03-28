<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col.mx-auto(md="8")
        v-card
          v-card-title {{ $t('notifications.name') }}
            v-spacer
            notifications-menu(:notifications="notifications")
          v-card-text
            mutation-result-alert(ref="mutationResultAlert")
            notifications-view(:notifications="notifications")
</template>

<script lang="ts">
import { ApolloError } from 'apollo-client'
import type { ComputedRef, PropType } from '#app'
import { defineComponent, inject, provide, ref, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { NotificationType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationResultAlert from '~/components/common/MutationResultAlert.vue'
import NotificationsMenu from '~/components/notifications/NotificationsMenu.vue'
import NotificationsView from '~/components/notifications/NotificationsView.vue'

export default defineComponent({
  components: { BreadCrumbs, MutationResultAlert, NotificationsMenu, NotificationsView },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup () {
    const { t } = useI18n()
    useNuxt2Meta({ title: t('notifications.name') as string })

    const mutationResultAlert = ref<InstanceType<typeof MutationResultAlert> | null>(null)

    const setApolloError = (error: ApolloError): void => {
      mutationResultAlert.value.setApolloError(error)
    }

    provide<(error: ApolloError) => void>('setAlertApolloError', setApolloError)
    const notifications: ComputedRef<NotificationType[]> = inject<ComputedRef<NotificationType[]>>('notifications')

    return { notifications, mutationResultAlert }
  }
})
</script>
