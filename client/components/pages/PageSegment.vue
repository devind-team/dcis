<template lang="pug">
  v-row
    v-col(v-if="segment.name" cols="12" :class="`text-${align[segment.align]}`")
      .text-h4.text-md-h2 {{ segment.name }}
    page-segment-element(
      v-slot="{ represent, pages }"
      v-for="el in segment.elements"
      :key="el.id"
      :segment-element="el"
    )
      template(v-if="pages.length")
        page-grid(v-if="represent === 'grid'" :pages="pages")
        page-card(v-else-if="represent === 'card'" :pages="pages")
        page-list(v-else-if="represent === 'list'" :pages="pages")
        page-slider(v-else-if="represent === 'slider'" :pages="pages")
        v-alert(v-else type="info") {{ $t('pages.components.pageSegment.noType', { represent }) }}
      v-alert(
        v-else
        type="info"
        v-html="$t('pages.components.pageSegment.noPages', { sectionNumber: el.pageKind.name })"
      )
</template>

<script lang="ts">

import { defineComponent, PropType } from '#app'
import { SegmentAlign, SegmentType, SegmentView } from '~/types/graphql'
import PageSegmentElement from '~/components/pages/PageSegmentElement.vue'
import PageSlider from '~/components/pages/views/PageSlider.vue'
import PageList from '~/components/pages/views/PageList.vue'
import PageCard from '~/components/pages/views/PageCard.vue'
import PageGrid from '~/components/pages/views/PageGrid.vue'

export default defineComponent({
  components: { PageSegmentElement, PageSlider, PageList, PageCard, PageGrid },
  props: {
    segment: { type: Object as PropType<SegmentType>, required: true }
  },
  setup () {
    const align: Record<SegmentAlign, string> = {
      A_0: 'left',
      A_1: 'center',
      A_2: 'right'
    }
    const view: Record<SegmentView, string> = {
      A_0: 'empty',
      A_1: 'card'
    }
    return { align, view }
  }
})
</script>
