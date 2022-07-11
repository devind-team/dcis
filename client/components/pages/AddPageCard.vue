<template lang="pug">
v-card(
  :to="localePath({ name: 'categories-categoryId-add_page', params: { categoryId: category.id } })"
  style="border: 1px rgba(0, 0, 0, 0.12) dashed"
  ripple outlined
)
  v-card-text.text-center
    v-icon mdi-plus
    | {{ $t('pages.page.addCardHeader') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { CategoryType } from '~/types/graphql'

export default defineComponent({
  props: {
    category: { type: Object as PropType<CategoryType>, required: true }
  }
})
</script>
