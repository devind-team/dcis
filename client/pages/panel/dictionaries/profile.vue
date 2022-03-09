<template lang="pug">
  universal-dictionary(
    @update-drawer="$emit('update-drawer')"
    :bread-crumbs="bc"
    :query="require('~/gql/core/queries/profiles.graphql')"
    :headers="['id', 'name', 'code', 'position', 'kind']"
    query-name="profiles"
  )
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'
import UniversalDictionary from '~/components/panel/UniversalDictionary.vue'

export default defineComponent({
  components: { UniversalDictionary },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.dictionary.profile') as string })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('panel.dictionary.profile') as string, to: localePath({ name: 'panel-dictionaries-profile' }), exact: true }
    ]))
    return { bc }
  }
})
</script>
