<template lang="pug">
  bread-crumbs(:items="bc")
    v-data-iterator(:items="categories" disable-pagination hide-default-footer)
      template(v-slot:default="{ items }")
        v-row
          v-col(v-for="category in items" :key="category.id" cols="12" sm="6" md="4" lg="4")
            v-card
              v-img(v-if="category.avatar" :src="`/${category.avatar}`" height="250")
              v-card-actions
                v-btn(
                  :to="localePath({ name: 'categories-categoryId', params: { categoryId: category.id } })"
                  text
                ) {{ category.text }}
                template(v-if="hasPerm(['pages.add_category', 'pages.change_category', 'pages.delete_category'], true)")
                  v-spacer
                  category-action(
                    :category="category"
                    :addCategoryUpdate="addCategoryUpdate"
                    :changeCategoryUpdate="changeCategoryUpdate"
                    :deleteCategoryUpdate="deleteCategoryUpdate"
                    add
                  )
              v-card-text
                v-list
                  v-list-item(
                    v-for="cat in category.children"
                    :key="cat.id"
                    :to="localePath({ name: 'categories-categoryId', params: { categoryId: cat.id } })"
                    exact
                  )
                    v-list-item-avatar(v-if="cat.avatar")
                      v-img(:src="`/${cat.avatar}`")
                    v-list-item-content
                      v-list-item-title {{ cat.text }}
                    v-list-item-action(v-if="hasPerm(['pages.change_category', 'pages.delete_category'], true)")
                      category-action(
                        :category="cat"
                        :changeCategoryUpdate="changeCategoryUpdate"
                        :deleteCategoryUpdate="deleteCategoryUpdate"
                        icon="mdi-dots-vertical")
          v-col(v-if="hasPerm('pages.add_category')" key="addCategory" cols="12" sm="6" md="4" lg="4")
            add-category(:update="addCategoryUpdate")
      template(#no-data)
        v-row
          v-col(v-if="hasPerm('pages.add_category')")
            add-category(:update="addCategoryUpdate")
          v-col(v-else) {{ $t('pages.category.noCategories') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { computed, ComputedRef, defineComponent, toRefs, useNuxt2Meta } from '#app'
import { HasPermissionFnType, useAuthStore } from '~/store'
import { useI18n, useQueryRelay } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  AddCategoryMutationPayload,
  CategoriesQuery,
  CategoriesQueryVariables,
  CategoryType, CategoryTypeEdge,
  ChangeCategoryMutationPayload,
  DeleteCategoryMutationPayload
} from '~/types/graphql'
import categoriesQuery from '~/gql/pages/queries/categories.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import CategoryAction from '~/components/pages/CategoryAction.vue'
import AddCategory from '~/components/pages/AddCategory.vue'

export type AddCategoryMutationResult = { data: { addCategory: AddCategoryMutationPayload } }
export type ChangeCategoryMutationResult = { data: { changeCategory: ChangeCategoryMutationPayload } }
export type DeleteCategoryMutationResult = { data: { deleteCategory: DeleteCategoryMutationPayload } }

export default defineComponent({
  components: { BreadCrumbs, CategoryAction, AddCategory },
  setup () {
    const authStore = useAuthStore()
    const { t, localePath } = useI18n()
    const { loginIn, hasPerm } = toRefs<{ loginIn: boolean, hasPerm: HasPermissionFnType }>(authStore)

    useNuxt2Meta({ title: t('pages.categories') as string })

    const { data: categories, loading, update } = useQueryRelay<CategoriesQuery, CategoriesQueryVariables, CategoryType>({
      document: categoriesQuery,
      variables: { isNull: true }
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      { text: t('index.main') as string, to: localePath({ name: 'index' }), exact: true },
      { text: t('pages.categories') as string, to: localePath({ name: 'categories' }), exact: true }
    ]))

    const addCategoryUpdate = (cache: DataProxy, result: AddCategoryMutationResult) => {
      const { success } = result.data.addCategory
      if (success) {
        update(cache, result, (dataCache, { data: { addCategory: { category } } }) => {
          category.parent
            ? dataCache.categories
              .edges.find((e: CategoryTypeEdge | any) => e.node.id === category.parent.id).node
              .children.push(category as any)
            : dataCache.categories.edges.push({ node: category, __typename: 'CategoryTypeEdge' } as any)
          return dataCache
        })
      }
    }

    const changeCategoryUpdate = (cache: DataProxy, result: ChangeCategoryMutationResult) => {
      const { success } = result.data.changeCategory
      if (success) {
        update(cache, result, (dataCache, { data: { changeCategory: { category } } }) => {
          dataCache.categories.edges = dataCache.categories.edges.map((e: CategoryTypeEdge | any) => {
            if (e.node?.id === category.id) {
              e.node = Object.assign(category, e.node!)
            }
            e.node!.children = e.node!.children.map((element: any) => {
              if (element!.id === category.id) {
                return Object.assign(category, element!)
              }
              return element
            })
            return e
          })
          return dataCache
        })
      }
    }

    const deleteCategoryUpdate = (cache: DataProxy, result: DeleteCategoryMutationResult, category: CategoryType) => {
      const { success } = result.data.deleteCategory
      if (success) {
        update(cache, result, (dataCache, _) => {
          dataCache.categories.edges = dataCache.categories.edges
            .filter((e: CategoryTypeEdge | any) => e.node.id !== category.id)
            .map((e: CategoryTypeEdge | any) => {
              e.node.children = e.node.children.filter((e: any) => e.id !== category.id)
              return e
            })
          return dataCache
        })
      }
    }

    return { bc, loginIn, hasPerm, categories, loading, addCategoryUpdate, changeCategoryUpdate, deleteCategoryUpdate }
  }
})
</script>
