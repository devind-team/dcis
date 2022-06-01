<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) Привилегии сбора {{ period.name }}
    v-card(flat)
      v-card-text
        v-data-table(
          :items="privileges"
          :headers="headers"
          :loading="loading"
          hide-default-footer
        )
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n, useCommonQuery } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, PrivilegesQuery, PrivilegesQueryVariables } from '~/types/graphql'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Атрибуты', to: localePath({ name: 'dcis-periods-periodId-attributes' }), exact: true }
    ]))
    const { data: privileges, loading } = useCommonQuery<PrivilegesQuery, PrivilegesQueryVariables>({
      document: privilegesQuery
    })
    const headers: DataTableHeader[] = [
      { text: 'Описание привилегии', value: 'name' },
      { text: 'Ключ', value: 'key' }
    ]
    return { bc, headers, privileges, loading }
  }
})
</script>
