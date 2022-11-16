<template lang="pug">
nuxt-child(v-if="!loading" :breadCrumbs="bc" :category="category")
v-row(v-else)
  v-col.text-center #[v-progress-circular(color="primary" indeterminate)]
</template>

<script lang="ts">
import { ApolloQueryResult } from '@apollo/client'
import type { ComputedRef } from '#app'
import { computed, defineComponent, onUnmounted } from '#app'
import { useRoute } from '#imports'
import { useCommonQuery, useI18n, usePage } from '~/composables'
import { CategoryQuery, CategoryQueryVariables } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { usePageStore } from '~/stores'
import categoryQuery from '~/gql/pages/queries/category.graphql'

export default defineComponent({
  setup () {
    const route = useRoute()
    const { t, localePath } = useI18n()
    const { setActiveCategories } = usePageStore()
    const { flatCategories } = usePage()
    const { data: category, loading, onResult } = useCommonQuery<CategoryQuery, CategoryQueryVariables>({
      document: categoryQuery,
      variables: () => ({
        categoryId: route.params.categoryId
      })
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
    onUnmounted(() => { setActiveCategories(flatCategories.value) })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      const breadCrumbs: BreadCrumbsItem[] = []
      if (!loading.value) {
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
          to: localePath({ name: 'categories-categoryId', params: { categoryId: category.value.id } }),
          exact: true
        })
      }
      return [
        { text: t('index.main') as string, to: localePath({ name: 'index' }), exact: true },
        { text: t('pages.categories') as string, to: localePath({ name: 'categories' }), exact: true },
        ...breadCrumbs
      ]
    })
    return { bc, category, loading }
  }
})
</script>
