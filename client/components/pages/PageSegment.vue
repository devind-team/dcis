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
import Vue, { PropType } from 'vue'
import { Component, Prop } from 'vue-property-decorator'
import { SegmentType, SegmentAlign, SegmentView } from '~/types/graphql'
import PageSegmentElement from '~/components/pages/PageSegmentElement.vue'
import PageGrid from '~/components/pages/views/PageGrid.vue'
import PageCard from '~/components/pages/views/PageCard.vue'
import PageList from '~/components/pages/views/PageList.vue'
import PageSlider from '~/components/pages/views/PageSlider.vue'

@Component<PageSegment>({
  components: { PageSegmentElement, PageSlider, PageList, PageCard, PageGrid },
  computed: {
    align () : { [K in SegmentAlign]: string } {
      return {
        A_0: 'left',
        A_1: 'center',
        A_2: 'right'
      }
    },
    view (): { [K in SegmentView]: string } {
      return {
        A_0: 'empty',
        A_1: 'card'
      }
    }
  }
})
export default class PageSegment extends Vue {
  @Prop({ required: true, type: Object as PropType<SegmentType> }) segment!: SegmentType
}
</script>
