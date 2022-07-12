<template lang="pug">
v-navigation-drawer(v-model="drawer" app temporary style="z-index: 11")
  v-list
    v-list-item(
      v-for="category in categories"
      :key="category.id"
      :to="localePath({ name: 'categories-categoryId', params: { categoryId: category.id } })"
      :class="{'v-list-item--active': activeCategories.map(e => e.id).includes(category.id) }"
      text) {{ category.text }}
</template>

<script lang="ts">
import { useVModel } from '@vueuse/core'
import type { Ref } from '#app'
import { defineComponent } from '#app'
import { useQueryRelay } from '~/composables'
import { usePageStore } from '~/stores'
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
    const { activeCategories } = usePageStore()
    const drawer: Ref<boolean> = useVModel(props, 'value', emit)
    const { data: categories } = useQueryRelay<CategoriesQuery, CategoriesQueryVariables, CategoryType>({
      document: categoriesQuery,
      variables: { isNull: true }
    })
    return { categories, activeCategories, drawer }
  }
})
</script>
