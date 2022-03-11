<template lang="pug">
  bread-crumbs(:items="bc")
    v-card
      v-card-title Настройки пользователя
      v-card-subtitle {{ project.name }}
      v-card-text
        pre {{ project }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { ProjectType } from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { useI18n } from '~/composables'

export default defineComponent({
  components: { BreadCrumbs },
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
