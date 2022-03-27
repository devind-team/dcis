<template lang="pug">
  v-card
    v-card-title {{ page.title }}
    v-card-text
      page-sections(:page="page")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { PageType, UserType } from '~/types/graphql'
import PageSections from '~/components/pages/PageSections.vue'

export default defineComponent({
  components: { PageSections },
  props: {
    page: { type: Object as PropType<PageType & { user: UserType }>, required: true }
  }
})
</script>
