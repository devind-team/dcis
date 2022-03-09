<template lang="pug">
  page-container(:bread-crumbs="bc" :category="category" :loading="loading")
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
import { ApolloQueryResult } from '@apollo/client'
import type { ComputedRef } from '#app'
import { defineComponent, useRoute, computed, onUnmounted, useNuxt2Meta } from '#app'
import { useCommonQuery, useI18n, usePage } from '~/composables'
import { useAuthStore, usePageStore } from '~/store'
import { CategoryQuery, CategoryQueryVariables } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import categoryQuery from '~/gql/pages/queries/category.graphql'
import PageContainer from '~/components/pages/PageContainer.vue'
import CategoryPages from '~/components/pages/CategoryPages.vue'
import PageView from '~/components/pages/PageView.vue'
import PageGrid from '~/components/pages/views/PageGrid.vue'
import PageCard from '~/components/pages/views/PageCard.vue'

export type ResultCategoryType = { data: any, loading: true }

export default defineComponent({
  components: { PageCard, PageGrid, PageView, PageContainer, CategoryPages },
  setup () {
    const route = useRoute()
    const { t, localePath } = useI18n()
    const { hasPerm } = useAuthStore()
    const { setActiveCategories } = usePageStore()
    const { flatCategories } = usePage()

    const { data: category, loading, onResult } = useCommonQuery<CategoryQuery, CategoryQueryVariables>({
      document: categoryQuery,
      variables: () => ({
        categoryId: route.params.categoryId
      }),
      options: {
        fetchPolicy: 'cache-and-network'
      }
    })
    onResult((params: ApolloQueryResult<CategoryQuery>) => {
      const { data, loading } = params
      if (!loading) {
        const activeCategories: string[] = data.category.parent
          ? [data.category.parent.id, data.category.id]
          : [data.category.id]
        setActiveCategories(flatCategories.value, activeCategories)
      }
    })
    useNuxt2Meta(() => ({ title: !loading.value ? category.value.text : t('loading') as string }))
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      const breadCrumbs: BreadCrumbsItem[] = []
      if (!loading) {
        if (category.value.parent) {
          breadCrumbs.push({
            text: category.value.parent.text,
            to: localePath({
              name: 'categories-categoryId',
              params: { categoryId: category.value.parent.id }
            }),
            exact: true
          })
        }
        breadCrumbs.push({
          text: category.value.text,
          to: localePath({ name: 'categories-categoryId', params: { categoryId: category.value.id } })
        })
      }
      return [
        { text: t('index.main') as string, to: localePath({ name: 'index' }), exact: true },
        { text: t('pages.categories') as string, to: localePath({ name: 'categories' }), exact: true },
        ...breadCrumbs
      ]
    })

    onUnmounted(() => { setActiveCategories(flatCategories.value) })

    return { bc, category, loading, hasPerm }
  }
})
</script>
