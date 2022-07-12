<template lang="pug">
v-container(v-bind="$attrs")
  v-breadcrumbs.px-0(:items="links")
    template(#divider)
      v-icon mdi-chevron-double-right
  slot
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'

export default defineComponent({
  props: {
    items: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const links: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => {
      if (localePath({ path: props.items[0].to }) === localePath({ path: '/' })) {
        return props.items
      }
      return [
        { text: t('index.main') as string, disabled: false, to: localePath('index') },
        ...props.items
      ]
    })
    return { links }
  }
})
</script>
