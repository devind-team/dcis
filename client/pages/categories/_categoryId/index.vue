<template lang="pug">
page-container(:bread-crumbs="breadCrumbs" :category="category")
  template(#header)
    .text-h4.text-md-h2 {{ category.text }}
  template(#default)
    category-pages(:category="category")
      page-view(
        v-slot="{ items, view }"
        :category="category"
        :allow-add="hasPerm('pages.add_page')"
        allow-search
        allow-loading
      )
        page-card(v-if="view === 'card'" :pages="items")
        page-grid(v-else :pages="items")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent, toRef, useNuxt2Meta } from '#app'
import { useAuthStore } from '~/stores'
import { CategoryType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import PageContainer from '~/components/pages/PageContainer.vue'
import CategoryPages from '~/components/pages/CategoryPages.vue'
import PageView from '~/components/pages/PageView.vue'
import PageGrid from '~/components/pages/views/PageGrid.vue'
import PageCard from '~/components/pages/views/PageCard.vue'

export default defineComponent({
  components: { PageCard, PageGrid, PageView, PageContainer, CategoryPages },
  props: {
    category: { type: Object as PropType<CategoryType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const authStore = useAuthStore()
    const hasPerm = toRef(authStore, 'hasPerm')

    useNuxt2Meta(() => ({ title: props.category.text }))

    return { hasPerm }
  }
})
</script>
