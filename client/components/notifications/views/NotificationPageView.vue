<template lang="pug">
  v-card
    v-card-title {{ page.title }}
    v-card-text
      page-sections(:page="page")
</template>

<script lang="ts">
import Vue, { AsyncComponent, PropType } from 'vue'
import { Component, Prop } from 'vue-property-decorator'
import { PageType } from '~/types/graphql'

const PageSections: AsyncComponent = () => import('~/components/pages/PageSections.vue')

@Component<NotificationPageView>({
  components: { PageSections }
})
export default class NotificationPageView extends Vue {
  @Prop({ type: Object as PropType<PageType>, required: true }) page!: PageType
}
</script>
