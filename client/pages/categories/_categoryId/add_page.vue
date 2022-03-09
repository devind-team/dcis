<template lang="pug">
  page-container(:bread-crumbs="bc" :category="category" :loading="loading")
    template(#header)
      .text-h4.text-md-h2 {{ $t('pages.page.add.header') }}
    template(#default)
      v-row
        v-col
          add-page(:category="category")
</template>

<script lang="ts">
import { ApolloQueryResult } from '@apollo/client'
import { computed, ComputedRef, defineComponent, onUnmounted, useNuxt2Meta, useRoute } from '#app'
import { useCommonQuery, useI18n, usePage } from '~/composables'
import { useAuthStore, usePageStore } from '~/store'
import { CategoryQuery, CategoryQueryVariables } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import categoryQuery from '~/gql/pages/queries/category.graphql'
import CategoryPages from '~/components/pages/CategoryPages.vue'
import PageContainer from '~/components/pages/PageContainer.vue'
import AddPage from '~/components/pages/AddPage.vue'

export default defineComponent({
  components: { AddPage, PageContainer, CategoryPages },
  setup () {
    const { t, localePath } = useI18n()
    const route = useRoute()

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
        const { category } = data
        const activeCategories: string[] = category.parent ? [category.parent.id, category.id] : [category.id]
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
        breadCrumbs.push({
          text: t('pages.page.add.header') as string,
          to: localePath({
            name: 'categories-categoryId-add_page',
            params: { categoryId: category.value.id }
          }),
          exact: true
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
