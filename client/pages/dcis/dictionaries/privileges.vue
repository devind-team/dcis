<template lang="pug">
universal-dictionary(
  @update-drawer="$emit('update-drawer')"
  :bread-crumbs="bc"
  :query="require('~/gql/dcis/queries/privileges.graphql')"
  :headers="['id', 'name', 'key', 'createdAt']"
  :convert-item="{ createdAt: dateTimeHM }"
  query-name="privileges"
)
</template>

<script lang="ts">
import type { PropType, ComputedRef } from '#app'
import { defineComponent, computed, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useFilters, useI18n } from '~/composables'
import UniversalDictionary from '~/components/dcis/dictionaries/UniversalDictionary.vue'
export default defineComponent({
  components: { UniversalDictionary },
  middleware: ['auth'],
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: t('dictionaries.privileges.header') as string })
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dictionaries.privileges.header') as string,
        to: localePath({ name: 'dcis-dictionaries-privileges' }),
        exact: true
      }
    ]))
    return { bc, dateTimeHM }
  }
})
</script>
