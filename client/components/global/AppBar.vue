<template lang="pug">
v-app-bar(app clipped-left)
  v-app-bar-nav-icon(v-show="$vuetify.breakpoint.smAndDown" @click="drawer = !drawer")
  slot(name="icon")
    v-img(:src="$getSettingValue('APP_ICON') || '/icon.png'" max-height="40" max-width="40")
  v-toolbar-title.ml-2
    slot(name="title")
      nuxt-link(:to="localePath({ name: 'index' })" style="text-decoration: none") {{ $getSettingValue('APP_NAME') }}
  v-spacer
  slot(name="middle")
    v-toolbar-items(v-show="$vuetify.breakpoint.mdAndUp")
      v-btn(
        v-for="category in categories"
        :key="category.id"
        :to="localePath({ name: 'categories-categoryId', params: { categoryId: category.id } })"
        :class="{ 'v-btn--active': activeCategories.map(e => e.id).includes(category.id) }"
        text
      ) {{ category.text }}
  v-spacer
  v-toolbar-items
    template(v-if="loginIn")
      notification(v-if="$vuetify.breakpoint.smAndUp")
      v-btn(v-else :to="localePath({ name: 'notifications' })" icon)
        v-icon mdi-bell
      avatar-menu
    template(v-else)
      slot(name="notAuthorized")
        v-btn(:to="localePath({ name: 'auth-login' })" text) {{ $t('auth.login.login') }}
</template>

<script lang="ts">
import { useVModel } from '@vueuse/core'
import type { Ref } from '#app'
import { defineComponent, toRef } from '#app'
import { useAuthStore, usePageStore } from '~/stores'
import { useQueryRelay } from '~/composables'
import { CategoriesQuery, CategoriesQueryVariables, CategoryType } from '~/types/graphql'
import categoriesQuery from '~/gql/pages/queries/categories.graphql'
import Notification from '~/components/global/Notification.vue'
import AvatarMenu from '~/components/global/AvatarMenu.vue'

export default defineComponent({
  components: { Notification, AvatarMenu },
  props: {
    value: { type: Boolean, required: true }
  },
  setup (props, { emit }) {
    const authStore = useAuthStore()
    const pageStore = usePageStore()
    const activeCategories: Readonly<Ref<CategoryType[]>> = toRef(pageStore, 'activeCategories')

    const loginIn: Readonly<Ref<boolean>> = toRef(authStore, 'loginIn')
    const drawer: Ref<boolean> = useVModel(props, 'value', emit)

    const { data: categories } = useQueryRelay<CategoriesQuery, CategoriesQueryVariables, CategoryType>({
      document: categoriesQuery,
      variables: { isNull: true }
    })
    return { categories, activeCategories, drawer, loginIn }
  }
})
</script>
