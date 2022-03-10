<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    v-row
      v-col Its work!
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'

export default defineComponent({
  components: { BreadCrumbs },
  middleware: 'auth',
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  }
})
</script>
