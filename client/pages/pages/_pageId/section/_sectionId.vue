<template lang="pug">
  bread-crumbs(:items="bc")
    .text-h4.text-md-h2.mb-7 {{ page.title }}
    change-section-text(v-if="section.kind === sectionKind.TEXT" :section="section" @done="updateSection")
    change-section-gallery(v-else-if="section.kind === sectionKind.GALLERY" :section="section" @done="updateSection")
    change-section-files(v-else-if="section.kind === sectionKind.FILES" :section="section" @done="updateSection")
</template>

<script lang="ts">
import { Context } from '@nuxt/types'
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { useNuxt2Meta } from '#app'
import {
  PageQuery,
  PageQueryVariables,
  PageType,
  SectionInterface
} from '~/types/graphql'
import { BreadCrumbsItem, PageKindChoices } from '~/types/devind'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import ChangeSectionGallery from '~/components/pages/sections/change/ChangeSectionGallery.vue'
import ChangeSectionFiles from '~/components/pages/sections/change/ChangeSectionFiles.vue'
import ChangeSectionText from '~/components/pages/sections/change/ChangeSectionText.vue'

export const sectionKind: PageKindChoices = {
  TEXT: 0,
  GALLERY: 1,
  FILES: 2,
  PROFILES: 3,
  SLIDERS: 4,
  FORM: 5,
  JUPYTER: 6,
  DATASET: 7
}

export default defineComponent({
  components: { ChangeSectionFiles, ChangeSectionGallery, ChangeSectionText, BreadCrumbs },
  validate ({ params }: Context): boolean {
    return /^\d+$/.test(params.sectionId)
  },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    page: { type: Object as PropType<PageType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const route = useRoute()
    useNuxt2Meta({ title: t('pages.section.change') as string })

    const section = computed<SectionInterface>(() => ({
      ...props.page.sections.find((e: any) => e.id === Number(route.params.sectionId))
    }))

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('pages.section.editSection') as string,
        to: localePath({
          name: 'pages-pageId-section-sectionId',
          params: { pageId: props.page.id, sectionId: section!.value.id as unknown as string }
        }),
        exact: true
      }
    ]))

    const updateSection = (store: DataProxy, section: SectionInterface) => {
      const data: PageQuery = store.readQuery<PageQuery, PageQueryVariables>({
        query: require('~/gql/pages/queries/page.graphql'),
        variables: { pageId: props.page.id }
      })!
      const tmpData = data.page.sections.find(x => x?.id === section.id)
      // @ts-ignore
      const index = data.page.sections.indexOf(tmpData)
      // @ts-ignore
      data.page.sections[index] = { ...tmpData, ...section }
      store.writeQuery({
        query: require('~/gql/pages/queries/page.graphql'),
        variables: { pageId: props.page.id },
        data
      })
    }

    return { section, bc, sectionKind, updateSection }
  }
})
</script>
