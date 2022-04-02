<template lang="pug">
  bread-crumbs(:items="bc")
    .text-h4.text-md-h2.mb-7 {{ page.title }}
    add-section-text(v-if="$route.query.kind==='text'" :page="page" @done="updatePage")
    add-section-gallery(v-else-if="$route.query.kind==='gallery'" :page="page" @done="updatePage")
    add-section-files(v-else-if="$route.query.kind==='files'" :page="page" @done="updatePage")
</template>

<script lang="ts">
import { Context } from '@nuxt/types'
import { DataProxy } from 'apollo-cache'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta, useRoute } from '#app'
import {
  PageQuery,
  PageQueryVariables,
  PageType,
  SectionInterface
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import AddSectionFiles from '~/components/pages/sections/add/AddSectionFiles.vue'
import AddSectionGallery from '~/components/pages/sections/add/AddSectionGallery.vue'
import AddSectionText from '~/components/pages/sections/add/AddSectionText.vue'

export default defineComponent({
  components: { AddSectionFiles, AddSectionGallery, AddSectionText, BreadCrumbs },
  validate ({ query }: Context): boolean {
    return ['text', 'gallery', 'files'].includes(query.kind as string)
  },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    page: { type: Object as PropType<PageType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()
    useNuxt2Meta({ title: t('pages.section.addSection') as string })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('pages.section.addSection') as string,
        to: localePath({ name: 'pages-pageId-section-add', query: route.query }),
        exact: true
      }
    ]))

    const updatePage = (store: DataProxy, section: SectionInterface) => {
      const data: PageQuery = store.readQuery<PageQuery, PageQueryVariables>({
        query: require('~/gql/pages/queries/page.graphql'),
        variables: { pageId: props.page.id }
      })!
      // @ts-ignore
      data.page.sections.push(section)
      store.writeQuery({
        query: require('~/gql/pages/queries/page.graphql'),
        variables: { pageId: props.page.id },
        data
      })
    }

    return { bc, updatePage }
  }
})
</script>
