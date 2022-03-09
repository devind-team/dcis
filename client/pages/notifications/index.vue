<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col.mx-auto(md="8")
        v-card
          v-card-title {{ t('name') }}
            v-spacer
            notifications-menu(:notifications="layoutInstance.notifications")
          v-card-text
            mutation-result-alert(ref="mutationResultAlert")
            notifications-view(:notifications="layoutInstance.notifications")
</template>

<script lang="ts">
import { AsyncComponent, PropType } from 'vue'
import { defineComponent } from '#app'
import { mapGetters } from 'vuex'
import { MetaInfo } from 'vue-meta'
import { ApolloError } from 'apollo-client'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import MutationResultAlert from '~/components/common/MutationResultAlert.vue'
const NotificationsMenu: AsyncComponent = () => import('~/components/notifications/NotificationsMenu.vue')
const NotificationsView: AsyncComponent = () => import('~/components/notifications/NotificationsView.vue')

export default defineComponent({
  components: { BreadCrumbs, MutationResultAlert, NotificationsMenu, NotificationsView },
  inject: ['layoutInstance'],
  provide () {
    return {
      setAlertApolloError: this.setApolloError,
    }
  },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  computed: mapGetters({ user: 'auth/user' }),
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
  },
  head (): MetaInfo {
    return { title: this.t('name') } as MetaInfo
  }
})


</script>
