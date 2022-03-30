<template lang="pug">
  left-navigator-container(:bread-crumbs="bc"  @update-drawer="$emit('update-drawer')")
    template(#header) Настройки пользователя
    pre {{ project }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { ProjectType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройки пользователя', to: localePath({ name: 'dcis-projects-projectId-accounts' }), exact: true }
    ]))

    return { bc }
  }
})
</script>
