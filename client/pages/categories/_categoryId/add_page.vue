<template lang="pug">
  page-container(:bread-crumbs="breadCrumbs" :category="category")
    template(#header)
      .text-h4.text-md-h2.mb-2 {{ $t('pages.page.add.header') }}
    add-page(:category="category")
</template>

<script lang="ts">
import { PropType, useNuxt2Meta } from '#app'
import { useAuthStore } from '~/store'
import { CategoryType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import AddPage from '~/components/pages/AddPage.vue'
import CategoryPages from '~/components/pages/CategoryPages.vue'
import PageContainer from '~/components/pages/PageContainer.vue'

export default defineComponent({
  components: { AddPage, PageContainer, CategoryPages },
  middleware: 'auth',
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
