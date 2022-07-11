<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  v-row
    v-col(style="position: relative")
      slot(name="header")
      v-app-bar-nav-icon(v-show="$vuetify.breakpoint.smAndDown" @click="drawer = true" absolute right top)
  category-right-navigator(v-model="drawer" :categories="category.nc")
  slot
</template>
<script lang="ts">
import type { PropType, Ref } from '#app'
import { defineComponent, ref } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { CategoryType } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import CategoryRightNavigator from '~/components/pages/CategoryRightNavigator.vue'

export default defineComponent({
  components: { BreadCrumbs, CategoryRightNavigator },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    category: { type: Object as PropType<CategoryType>, required: true }
  },
  setup () {
    const drawer: Ref<boolean> = ref<boolean>(false)
    return { drawer }
  }
})
</script>
