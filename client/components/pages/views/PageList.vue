<template lang="pug">
v-row
  v-col
    v-list(two-line)
      v-list-item(v-for="page in pages" :key="page.id" :to="localePath({ name: 'pages-pageId', params: { pageId: page.id }})")
        v-list-item-avatar(v-if="page.avatar")
          v-avatar(tile)
            v-img(:src="`/${page.avatar}`" height="220")
        v-list-item-content
          v-list-item-title {{ page.title }}
          v-list-item-subtitle.caption {{ $filters.dateTimeHM(page.updatedAt) }}
          v-list-item-subtitle.px-0(v-if="page.tags.length")
            v-chip.mr-2(v-for="tag in page.tags" :key="tag.id" small) {{ tag.name }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { PageType } from '~/types/graphql'
import { useFilters } from '~/composables'
import AddPage from '~/components/pages/AddPage.vue'

export default defineComponent({
  components: { AddPage },
  props: {
    pages: { type: Array as PropType<PageType[]>, required: true }
  },
  setup () {
    const { dateTimeHM } = useFilters()
    return { dateTimeHM }
  }
})
</script>
