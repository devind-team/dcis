<template lang="pug">
v-data-iterator(:items="pages" :loading="loading" disable-pagination hide-default-footer)
  template(#header v-if="allowSearch")
    v-row(align="center")
      v-col(cols="12" md="8")
        v-text-field(v-model="search" :label="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right(v-if="!loading && totalCount" cols="12" md="4")
        | {{ $t('pages.components.pageView.showOf', { count, totalCount }) }}
        v-btn-toggle.ml-2(v-model="view")
          v-btn(value="grid")
            v-icon mdi-view-grid
          v-btn(value="card")
            v-icon mdi-view-list
  template(#default="{ items }")
    v-row
      v-col(v-if="allowAdd" cols="12")
        add-page-card(:category="category")
    slot(:items="items" :view="view")
  template(#footer)
    v-row(v-if="loading")
      v-col.text-center #[v-progress-circular(color="primary" indeterminate)]
  template(#no-data)
    .font-italic(v-if="search && search.length") {{ $t('pages.components.pageView.noResults') }}
    v-row(v-else)
      v-col
        v-alert(type="info") {{ $t('pages.components.pageView.noPages') }}
      v-col(v-if="allowAdd" v-bind="breakPointsGrid")
        add-page-card(:category="category")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent, ref, unref } from '#app'
import { CategoryType, PagesQuery, PagesQueryVariables, PageType } from '~/types/graphql'
import { useCursorPagination, useDebounceSearch, useQueryRelay } from '~/composables'
import pagesQuery from '~/gql/pages/queries/pages.graphql'
import AddPageCard from '~/components/pages/AddPageCard.vue'

export default defineComponent({
  components: { AddPageCard },
  props: {
    category: { type: Object as PropType<CategoryType>, default: null },
    kindId: { type: String, default: null },
    pageSize: { type: Number, default: 24 },
    allowSearch: { type: Boolean, default: false },
    allowLoading: { type: Boolean, default: false },
    allowAdd: { type: Boolean, default: false }
  },
  setup (props) {
    const breakPointsGrid: Record<string, number> = { cols: 12, md: 6, lg: 6, xl: 4 }
    const view = ref<string>('grid')
    const { search, debounceSearch } = useDebounceSearch()
    const {
      data: pages,
      loading,
      pagination: { totalCount, count }
    } = useQueryRelay<PagesQuery, PagesQueryVariables, PageType>({
      document: pagesQuery,
      variables: () => ({
        categoryId: props.category?.id,
        kindId: props.kindId,
        search: unref(debounceSearch)
      })
    }, {
      pagination: useCursorPagination({ pageSize: props.pageSize }),
      fetchScroll: typeof document === 'undefined' ? null : document
    })
    return { breakPointsGrid, view, search, pages, loading, count, totalCount }
  }
})
</script>
