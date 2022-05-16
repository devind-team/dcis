<template lang="pug">
  v-row
    v-col(v-bind="breakPointsLeftGrid")
      slot
    v-col(v-if="showLeft" v-show="$vuetify.breakpoint.mdAndUp" v-bind="breakPointsRightGrid")
      v-card.mt-0
        v-card-text.pa-0
          v-list
            v-list-item(
              v-for="cat in category.nc"
              :key="cat.id"
              :to="localePath({ name: 'categories-categoryId', params: { categoryId: cat.id } })"
              :class="{'v-list-item--active': activeCategories.map(e => e.id).includes(cat.id) }"
            )
              v-list-item-content
                v-list-item-title {{ cat.text }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { usePageStore } from '~/stores'
import { CategoryType } from '~/types/graphql'
import PageList from '~/components/pages/views/PageGrid.vue'

export type GridMetricsType = {
  cols: number
  md: number
  lg: number
  xl: number
}

export default defineComponent({
  components: { PageList },
  props: {
    category: { required: true, type: Object as PropType<CategoryType> }
  },
  setup (props) {
    const { activeCategories } = usePageStore()
    const showLeft: ComputedRef<boolean> = computed<boolean>(() => (props.category.nc.length !== 0))
    const breakPointsLeftGrid: ComputedRef<GridMetricsType> = computed<GridMetricsType>(() => ({
      cols: 12,
      md: showLeft.value ? 8 : 12,
      lg: showLeft.value ? 8 : 12,
      xl: showLeft.value ? 9 : 12
    }))
    const breakPointsRightGrid: ComputedRef<GridMetricsType> = computed<GridMetricsType>(() => ({
      cols: 12,
      md: showLeft ? 4 : 12,
      lg: showLeft ? 4 : 12,
      xl: showLeft ? 3 : 12
    }))
    return { activeCategories, showLeft, breakPointsLeftGrid, breakPointsRightGrid }
  }
})
</script>
