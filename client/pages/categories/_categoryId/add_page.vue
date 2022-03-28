<template lang="pug">
  page-container(:bread-crumbs="bc" :category="category")
    template(#header)
      .text-h4.text-md-h2.mb-2 {{ $t('pages.page.add.header') }}
    template(#default)
      add-page(:category="category")
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { useAuthStore } from '~/store'
import { CategoryType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import CategoryPages from '~/components/pages/CategoryPages.vue'
import PageContainer from '~/components/pages/PageContainer.vue'
import AddPage from '~/components/pages/AddPage.vue'

export default defineComponent({
  components: { AddPage, PageContainer, CategoryPages },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    category: { type: Object as PropType<CategoryType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const { hasPerm } = useAuthStore()

    useNuxt2Meta(() => ({ title: props.category.text }))

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      return [
        ...props.breadCrumbs,
        {
          text: t('pages.page.add.header') as string,
          to: localePath({
            name: 'categories-categoryId-add_page',
            params: { categoryId: props.category.id }
          }),
          exact: true
        }
      ]
    })
    return { bc, hasPerm }
  }
})
</script>
