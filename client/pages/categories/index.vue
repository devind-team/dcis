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
                template(
                  v-if="hasPerm(['pages.add_category', 'pages.change_category', 'pages.delete_category'], true)"
                  )
                  v-spacer
                  category-action(
                    :category="category"
                    :addCategoryUpdate="addCategory"
                    :changeCategoryUpdate="changeCategory"
                    :deleteCategoryUpdate="deleteCategory" add)
              v-card-text
                v-list
                  v-list-item(
                    v-for="cat in category.children"
                    :key="cat.id"
                    :to="localePath({ name: 'categories-categoryId', params: { categoryId: cat.id } })"
                    exact)
                    v-list-item-avatar(v-if="cat.avatar")
                      v-img(:src="`/${cat.avatar}`")
                    v-list-item-content
                      v-list-item-title {{ cat.text }}
                    v-list-item-action(v-if="hasPerm(['pages.change_category', 'pages.delete_category'], true)")
                      category-action(
                        :category="cat"
                        :changeCategoryUpdate="changeCategory"
                        :deleteCategoryUpdate="deleteCategory"
                        icon="mdi-dots-vertical")
          v-col(v-if="hasPerm('pages.add_category')" key="addCategory" cols="12" sm="6" md="4" lg="4")
            add-category(:update="addCategory")
      template(#no-data)
        v-row
          v-col(v-if="hasPerm('pages.add_category')")
            add-category(:update="addCategory")
          v-col(v-else) {{ $t('pages.category.noCategories') }}
</template>

<script lang="ts">
import Vue, { AsyncComponent } from 'vue'
import { Component } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
import { mapGetters } from 'vuex'
import { DataProxy } from 'apollo-cache'
import categoriesQuery from '~/gql/pages/queries/categories.graphql'
import { BreadCrumbsItem } from '~/types/devind'
import {
  AddCategoryMutationPayload,
  CategoryType,
  CategoryTypeEdge
} from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
const CategoryAction: AsyncComponent = () => import('~/components/pages/CategoryAction.vue')
const AddCategory: AsyncComponent = () => import('~/components/pages/AddCategory.vue')

@Component({
  components: { BreadCrumbs, AddCategory, CategoryAction },
  computed: {
    ...mapGetters({ loginIn: 'auth/loginIn', hasPerm: 'auth/hasPerm' }),
    bc (): BreadCrumbsItem[] {
      return [
        { text: this.$t('index.main') as string, to: this.localePath({ name: 'index' }), exact: true },
        { text: this.$t('pages.categories') as string, to: this.localePath({ name: 'categories' }), exact: true }
      ]
    }
  },
  apollo: {
    categories: {
      query: categoriesQuery,
      variables: { isNull: true },
      update ({ categories }: any): CategoryType[] {
        return categories.edges.map((e: any) => e.node)
      }
    }
  },
  head (): MetaInfo {
    return { title: this.$t('pages.categories') as string } as MetaInfo
  }
})
export default class CategoryIndex extends Vue {
  categories!: CategoryType[]
  loginIn!: boolean
  hasPerm!: (permissions: string | string[], or?: boolean) => boolean

  /**
   * Добавляем новую категорию
   */
  addCategory (
    store: DataProxy,
    { data: { addCategory: { success, category } } }: { data: { addCategory: AddCategoryMutationPayload } }
  ) {
    if (success) {
      const data: any = store.readQuery({ query: categoriesQuery, variables: { isNull: true } })
      if (category?.parent) {
        data.categories.edges.find((e: CategoryTypeEdge) => e.node!.id === category?.parent!.id).node.children.push(category)
      } else {
        data.categories.edges.push({ node: category, __typename: 'CategoryTypeEdge' })
      }
      store.writeQuery({ query: categoriesQuery, variables: { isNull: true }, data })
    }
  }

  changeCategory (store: DataProxy, { data: { changeCategory: { success, category } } }: any) {
    if (success) {
      const data: any = store.readQuery({ query: categoriesQuery, variables: { isNull: true } })
      data.categories.edges = data.categories.edges.map((e: CategoryTypeEdge) => {
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
      store.writeQuery({ query: categoriesQuery, variables: { isNull: true }, data })
    }
  }

  /**
   * Удаляем категорию
   * @param store
   * @param success
   * @param category
   */
  deleteCategory (store: DataProxy, { data: { deleteCategory: { success } } }: any, category: CategoryType) {
    if (success) {
      const data: any = store.readQuery({ query: categoriesQuery, variables: { isNull: true } })
      data.categories.edges = data.categories.edges
        .filter((e: CategoryTypeEdge) => e.node?.id !== category.id)
        .map((e: CategoryTypeEdge) => {
          e.node!.children = e.node!.children.filter((e: any) => e!.id !== category.id)
          return e
        })
      store.writeQuery({ query: categoriesQuery, variables: { isNull: true }, data })
    }
  }
}
</script>
