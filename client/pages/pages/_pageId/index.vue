<template lang="pug">
page-container(v-if="!loading" :bread-crumbs="bc" :category="page && page.category")
  template(#header)
    .text-h4.text-md-h2 {{ loading ? $t('loading') : page.title }}
  category-pages(v-if="!loading" :category="page.category")
    v-card.pa-3
      page-sections(:page="page")
        template(#actions)
          page-actions(
            v-if="hasPerm(['pages.add_section', 'pages.change_page', 'pages.delete_page'], true)"
            :page="page"
          )
  v-row(v-else)
    v-col.text-center #[v-progress-circular(color="primary" indeterminate)]
</template>

<script lang="ts">
import { ApolloQueryResult } from '@apollo/client'
import type { ComputedRef } from '#app'
import { Ref, computed, defineComponent, onUnmounted, toRef, useNuxt2Meta } from '#app'
import { useRoute } from '#imports'
import { useCommonQuery, useI18n, usePage } from '~/composables'
import { HasPermissionFnType, useAuthStore, usePageStore } from '~/stores'
import { PageQuery, PageQueryVariables } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import pageQuery from '~/gql/pages/queries/page.graphql'
import PageContainer from '~/components/pages/PageContainer.vue'
import CategoryPages from '~/components/pages/CategoryPages.vue'
import PageSections from '~/components/pages/PageSections.vue'
import PageActions from '~/components/pages/PageActions.vue'

export default defineComponent({
  components: { PageActions, PageSections, CategoryPages, PageContainer },
  setup () {
    const route = useRoute()
    const { t, localePath } = useI18n()
    const authStore = useAuthStore()
    const { setActiveCategories } = usePageStore()
    const { flatCategories } = usePage()

    const hasPerm: Ref<HasPermissionFnType> = toRef(authStore, 'hasPerm')

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

    useNuxt2Meta(() => ({ title: loading.value ? t('loading') as string : page.value.title }))

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      const breadCrumbs: BreadCrumbsItem[] = []
      if (!loading.value) {
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
    return { bc, page, loading, hasPerm }
  }
})
</script>
