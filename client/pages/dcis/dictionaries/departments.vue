<template lang="pug">
universal-dictionary(
  @update-drawer="$emit('update-drawer')"
  :bread-crumbs="bc"
  :query="require('~/gql/dcis/queries/departments.graphql')"
  :headers="['id', 'name', 'code', 'createdAt']"
  :convert-item="{ createdAt: dateTimeHM }"
  query-name="departments"
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
    useNuxt2Meta({ title: t('dictionaries.departments.header') as string })
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dictionaries.departments.header') as string,
        to: localePath({ name: 'dcis-dictionaries-departments' }),
        exact: true
      }
    ]))
    return { bc, dateTimeHM }
  }
})
</script>
