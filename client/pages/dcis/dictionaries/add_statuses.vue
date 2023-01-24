<template lang="pug">
universal-dictionary(
  @update-drawer="$emit('update-drawer')"
  :bread-crumbs="bc"
  :query="require('~/gql/dcis/queries/add_statuses.graphql')"
  :headers="headers"
  query-name="addStatuses"
)
</template>

<script lang="ts">
import type { PropType, ComputedRef } from '#app'
import { defineComponent, computed, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'
import UniversalDictionary, { Header } from '~/components/dcis/dictionaries/UniversalDictionary.vue'
export default defineComponent({
  components: { UniversalDictionary },
  middleware: ['auth'],
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const headers: Header[] = [
      'id',
      'roles',
      'check',
      { name: 'fromStatus', value: 'fromStatus.name' },
      { name: 'toStatus', value: 'toStatus.name' }
    ]
    useNuxt2Meta({ title: t('dictionaries.addStatuses.header') as string })
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dictionaries.addStatuses.header') as string,
        to: localePath({ name: 'dcis-dictionaries-add_statuses' }),
        exact: true
      }
    ]))
    return { bc, headers }
  }
})
</script>
