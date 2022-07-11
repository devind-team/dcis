<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')" fluid)
  template(#header) {{ $t('panel.permissions') }}
  v-row(align="center")
    v-col(cols="12" md="8")
      v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
    v-col.text-right(cols="12" md="4") {{ $t('panel.ac.permissions.shownOf', { count: permissions && permissions.length }) }}.
  v-data-table(
    :headers="headers"
    :items="permissions"
    :loading="loading"
    :search="search"
    dense disable-pagination
    hide-default-footer
  )
    template(#item.contentType="{ item }") {{ item.contentType.appLabel }} / {{ item.contentType.model }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { Ref, ComputedRef, PropType } from '#app'
import { defineComponent, ref, computed, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { PermissionsQuery, PermissionsQueryVariables } from '~/types/graphql'
import { useI18n, useCommonQuery } from '~/composables'
import permissionsQuery from '~/gql/core/queries/permissions.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  permissions: ['auth.view_permission'],
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.permissions') as string })

    const search: Ref<string> = ref<string>('')

    const bc: ComputedRef<BreadCrumbsItem[]> = computed(() => ([
      ...props.breadCrumbs,
      { text: t('panel.permissions') as string, to: localePath({ name: 'panel-ac-permissions' }), exact: true }
    ]))
    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('panel.ac.permissions.tableHeaders.contentType') as string, value: 'contentType' },
      { text: t('panel.ac.permissions.tableHeaders.name') as string, value: 'name' },
      { text: t('panel.ac.permissions.tableHeaders.codename') as string, value: 'codename' }
    ]))

    const {
      loading,
      data: permissions
    } = useCommonQuery<PermissionsQuery, PermissionsQueryVariables>({
      document: permissionsQuery
    })

    return { search, bc, headers, loading, permissions }
  }
})
</script>
