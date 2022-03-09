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
import { Vue, Component, Prop } from 'vue-property-decorator'
import { BreadCrumbsItem } from '~/types/devind'
import { CategoryType } from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import CategoryRightNavigator from '~/components/pages/CategoryRightNavigator.vue'

@Component<PageContainer>({
  components: { BreadCrumbs, CategoryRightNavigator }
})
export default class PageContainer extends Vue {
  @Prop() breadCrumbs!: BreadCrumbsItem[]
  @Prop() category!: CategoryType
  @Prop({ default: false }) loading!: boolean

  drawer: boolean = false
}
</script>
