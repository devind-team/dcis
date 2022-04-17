<template lang="pug">
  bread-crumbs(:items="breadCrumbs")
    template(v-if="!loading")
      v-row
        v-col(style="position: relative")
          slot(name="header")
          v-app-bar-nav-icon(v-show="$vuetify.breakpoint.smAndDown" @click="drawer = true" absolute right top)
      category-right-navigator(v-model="drawer" :categories="category.nc")
      slot
    v-row(v-else)
      v-col.text-center #[v-progress-circular(color="primary" indeterminate)]
</template>
<script lang="ts">
import type { PropType, Ref } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { CategoryType } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import CategoryRightNavigator from '~/components/pages/CategoryRightNavigator.vue'

export default defineComponent({
  components: { BreadCrumbs, CategoryRightNavigator },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    category: { type: Object as PropType<CategoryType>, required: true },
    loading: { type: Boolean, required: true }
  },
  setup () {
    const drawer: Ref<boolean> = ref<boolean>(false)
    return { drawer }
  }
})
</script>
