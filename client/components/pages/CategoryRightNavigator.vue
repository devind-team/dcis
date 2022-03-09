<template lang="pug">
  v-navigation-drawer(app @input="drawer = $event" :value="drawer" width="350" temporary right)
    v-list
      v-list-item(
        v-for="category in categories"
        :key="category.id"
        :to="localePath({ name: 'categories-categoryId', params: { categoryId: category.id } })"
        :class="{'v-list-item--active': activeCategories.map(e => e.id).includes(category.id) }"
        ) {{ category.text }}
</template>

<script lang="ts">
import { useVModel } from '@vueuse/core'
import type { PropType, Ref } from '#app'
import { defineComponent } from '#app'
import { CategoryType } from '~/types/graphql'
import { usePageStore } from '~/store'

export default defineComponent({
  props: {
    value: { type: Boolean, required: true },
    categories: { type: Array as PropType<CategoryType[]>, required: true }
  },
  setup (props, { emit }) {
    const { activeCategories } = usePageStore()
    const drawer: Ref<boolean> = useVModel(props, 'value', emit)
    return { activeCategories, drawer }
  }
})
</script>
