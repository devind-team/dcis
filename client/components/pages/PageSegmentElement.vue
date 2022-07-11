<template lang="pug">
v-col(cols="12" :md="segmentElement.width")
  v-card(v-if="view[segmentElement.view] === 'card'")
    v-card-title {{ segmentElement.pageKind.name }}
    slot(:pages="segmentElement.pageKind.pages" :represent="represent[segmentElement.represent]")
  template(v-else)
    slot(:pages="segmentElement.pageKind.pages" :represent="represent[segmentElement.represent]")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { SegmentElementRepresent, SegmentElementType, SegmentElementView } from '~/types/graphql'

export default defineComponent({
  props: {
    segmentElement: { type: Object as PropType<SegmentElementType>, required: true }
  },
  setup () {
    const view: { [K in SegmentElementView]: string } = {
      A_0: 'empty',
      A_1: 'card'
    }

    const represent: { [K in SegmentElementRepresent]: string } = {
      A_0: 'grid',
      A_1: 'card',
      A_2: 'list',
      A_3: 'slider'
    }

    return { view, represent }
  }
})
</script>
