<template lang="pug">
  v-hover(v-slot="{ hover }")
    v-carousel(:cycle="!hover" delimiter-icon="mdi-minus" height="600")
      v-carousel-item(
        v-for="page in pages"
        :key="page.id"
        :to="localePath({ name: 'pages-pageId', params: { pageId: page.id }})"
        :src="`/${page.avatar}`"
        reverse-transition="fade-transition"
        transition="fade-transition")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { PageType } from '~/types/graphql'

export default defineComponent({
  props: {
    pages: { type: Array as PropType<PageType[]>, required: true }
  }
})
</script>
