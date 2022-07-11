<template lang="pug">
bread-crumbs(:items="breadCrumbs" :fluid="fluid")
  v-card
    v-card-title
      v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
      slot(name="header")
    v-card-subtitle
      slot(name="subheader")
    v-card-text
      slot
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export default defineComponent({
  components: { BreadCrumbs },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    fluid: { type: Boolean, default: false }
  }
})
</script>
