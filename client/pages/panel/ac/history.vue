<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')" fluid)
    template(#header) {{ $t('profile.history.name') }}
    v-row(align="center")
      v-col(cols="12" md="8")
        v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right.pr-5(cols="12" md="4") {{ $t('panel.ac.history.shownOf', { count, totalCount }) }}
    v-data-table(
      :headers="headers"
      :items="logRequests"
      :loading="loading"
      dense disable-pagination hide-default-footer)
      template(v-slot:item.user="{ item }")
        v-tooltip(bottom)
          template(v-slot:activator="{ on }")
            span(v-on="on") {{ item.session.user.lastName }} {{ item.session.user.firstName }} {{ item.session.user.sirName }}
          span {{ item.session.user.username }} / {{ item.session.user.email }}
      template(v-slot:item.createdAt="{ item }") {{ $filters.dateTimeHM(item.createdAt) }}
      template(v-slot:item.time="{ item }") {{ item.time.toFixed(3) }} с.
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { computed, defineComponent, toRef, useNuxt2Meta } from '#app'
import type { Ref, ComputedRef, PropType } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useCursorPagination, useDebounceSearch, useI18n, useQueryRelay } from '~/composables'
import { LogRequestsQuery, LogRequestsQueryVariables, LogRequestType } from '~/types/graphql'
import logGeneralRequestsQuery from '~/gql/core/queries/log_general_requests.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  permissions: 'devind_core.view_logrequest',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.groups') as string })

    const breadCrumbs: Ref<BreadCrumbsItem[]> = toRef(props, 'breadCrumbs')

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...breadCrumbs.value,
      { text: t('profile.history.name') as string, to: localePath({ name: 'panel-ac-history' }), exact: true }
    ]))
    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('panel.ac.history.tableHeaders.user') as string, value: 'user' },
      { text: t('panel.ac.history.tableHeaders.page') as string, value: 'page' },
      { text: t('panel.ac.history.tableHeaders.browser') as string, value: 'session.browser' },
      { text: t('panel.ac.history.tableHeaders.device') as string, value: 'session.device' },
      { text: t('panel.ac.history.tableHeaders.os') as string, value: 'session.os' },
      { text: t('panel.ac.history.tableHeaders.createdAt') as string, value: 'createdAt' },
      { text: t('panel.ac.history.tableHeaders.time') as string, value: 'time' }
    ]))

    const { search, debounceSearch } = useDebounceSearch()
    const {
      loading,
      pagination: { count, totalCount },
      data: logRequests
    } = useQueryRelay<LogRequestsQuery, LogRequestsQueryVariables, LogRequestType>({
      document: logGeneralRequestsQuery,
      variables: () => ({
        pageContains: debounceSearch.value
      }),
      options: { fetchPolicy: 'network-only' }
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    return {
      bc,
      search,
      headers,
      loading,
      count,
      totalCount,
      logRequests
    }
  }
})
</script>
