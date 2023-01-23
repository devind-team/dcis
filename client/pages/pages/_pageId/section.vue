<template lang="pug">
nuxt-child(v-if="!loading" :bread-crumbs="bc" :page="page")
</template>

<script lang="ts">
import { ApolloQueryResult } from '@apollo/client'
import type { ComputedRef } from '#app'
import { computed, defineComponent, onUnmounted } from '#app'
import { useRoute } from '#imports'
import { useCommonQuery, useI18n, usePage } from '~/composables'
import { usePageStore } from '~/stores'
import { PageQuery, PageQueryVariables } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import pageQuery from '~/gql/pages/queries/page.graphql'

export default defineComponent({
  setup () {
    const route = useRoute()
    const { t, localePath } = useI18n()
    const { setActiveCategories } = usePageStore()
    const { flatCategories } = usePage()

    const { data: page, loading, onResult } = useCommonQuery<PageQuery, PageQueryVariables>({
      document: pageQuery,
      variables: () => ({ pageId: route.params.pageId })
    })
    onResult((params: ApolloQueryResult<PageQuery>) => {
      const { data, loading } = params
      if (!loading) {
        const category = data.page.category
        const activeCategories: string[] = category.parent ? [category.parent.id, category.id] : [category.id]
        setActiveCategories(flatCategories.value, activeCategories)
      }
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      const breadCrumbs: BreadCrumbsItem[] = []
      if (!loading) {
        if (page.value.category && page.value.category.parent) {
          breadCrumbs.push({
            text: page.value.category.parent.text,
            to: localePath({
              name: 'categories-categoryId',
              params: { categoryId: page.value.category.parent.id }
            }),
            exact: true
          })
        }
        breadCrumbs.push({
          text: page.value.category.text,
          to: localePath({ name: 'categories-categoryId', params: { categoryId: page.value.category.id } }),
          exact: true
        })
        breadCrumbs.push({
          text: page.value.title,
          to: localePath({ name: 'pages-pageId', params: { pageId: page.value.id } }),
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
    return { bc, page, loading }
  }
})
</script>
