<template lang="pug">
  v-row
    v-col(v-for="page in pages" :key="page.id" v-bind="breakPointsGrid")
      v-hover(v-slot="{ hover }")
        v-card(:elevation="hover ? 5 : 1")
          v-img(v-if="page.avatar" :src="`/${page.avatar}`" height="220" contain)
          v-card-title
            nuxt-link(:to="localePath({ name: 'pages-pageId', params: { pageId: page.id }})"
              style="text-decoration: none; word-break: normal;") {{ page.title }}
          v-card-text(v-if="page.preview")
            editor-typography(:html="page.preview")
          v-divider
          v-card-text.px-0(v-if="page.tags.length")
            v-chip.ml-2(v-for="tag in page.tags" :key="tag.id" small) {{ tag.name }}
          v-card-actions
            nuxt-link.caption(
              :to="localePath({ name: 'categories-categoryId', params: { categoryId: page.category.id } })"
              style="text-decoration: none"
            ) {{ page.category.text }}
            v-spacer
            .caption {{ dateTimeHM(page.updatedAt) }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { PageType } from '~/types/graphql'
import { useFilters } from '~/composables'
import AddPage from '~/components/pages/AddPage.vue'
import EditorTypography from '~/components/common/editor/EditorTypography.vue'

export default defineComponent({
  components: { EditorTypography, AddPage },
  props: {
    pages: { type: Array as PropType<PageType[]>, required: true }
  },
  setup () {
    const { dateTimeHM } = useFilters()
    const breakPointsGrid: { [key: string]: number } = { cols: 12, md: 6, lg: 6, xl: 4 }
    return { dateTimeHM, breakPointsGrid }
  }
})
</script>
