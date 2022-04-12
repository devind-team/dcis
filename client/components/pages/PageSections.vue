<template lang="pug">
  v-data-iterator(:items="page.sections" disable-pagination hide-default-footer)
    template(#header)
      v-row(align="center" no-gutters)
        v-col
          span.caption(v-if="page.signature") {{ page.signature }}
          v-chip.mx-2(v-else-if="page.user" pill)
            v-avatar(v-if="page.user.avatar" left)
              v-img(:src="`/${page.user.avatar}`")
            | {{ `${page.user.lastName} ${page.user.firstName[0]}. ${page.user.sirName[0]}.` }}
          span.ml-4.caption {{ $filters.dateTimeHM(page.createdAt) }}
        v-col.text-right
          slot(name="actions")
      v-row(v-if="page.parallax && !!page.avatar")
        v-img(:src="`/${page.avatar}`" max-height="450" min-height="300" contain)
    //- Вывод секций странички
    template(#default="{ items }")
      template(v-for="section in page.sections")
        section-text(v-if="section.kind === sectionKind.TEXT" :key="section.id"  :page="page" :section="section")
        section-gallery(v-else-if="section.kind === sectionKind.GALLERY" :key="section.id" :page="page" :section="section")
        section-files(v-else-if="section.kind === sectionKind.FILES" :key="section.id" :page="page" :section="section")
    //- Вывод подвала странички
    template(#footer)
      v-row.mt-2(align="center")
        v-col(v-if="page.tags.length")
          v-chip.mr-2(v-for="tag in page.tags" :key="tag.id" small) {{ tag.name }}
        v-col.text-right
          v-icon(left) mdi-eye-outline
          | {{ page.views }}
    template(#no-data)
      v-alert(type="info") {{ $t('pages.components.pageSections.noSections') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { UserType, PageType } from '~/types/graphql'
import { PageKindChoices } from '~/types/devind'
import SectionText from '~/components/pages/sections/views/SectionText.vue'
import SectionGallery from '~/components/pages/sections/views/SectionGallery.vue'
import SectionFiles from '~/components/pages/sections/views/SectionFiles.vue'

export default defineComponent({
  components: { SectionFiles, SectionText, SectionGallery },
  props: {
    page: { type: Object as PropType<PageType & { user: UserType }>, required: true }
  },
  setup () {
    const sectionKind: PageKindChoices = {
      TEXT: 0,
      GALLERY: 1,
      FILES: 2,
      PROFILES: 3,
      SLIDERS: 4,
      FORM: 5,
      JUPYTER: 6,
      DATASET: 7
    }
    return { sectionKind }
  }
})
</script>
