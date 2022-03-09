<template lang="pug">
  v-card
    v-card-title {{ $t('profile.history.name') }}
      v-spacer
      .caption {{ $t('shownOf', { count, totalCount }) }}
    v-card-text
      v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-row
        v-col
          v-data-table(
            :headers="headers"
            :items="logRequests"
            :loading="loading"
            dense
            disable-pagination
            hide-default-footer
          )
            template(v-slot:item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
            template(v-slot:item.time="{ item }") {{ item.time.toFixed(3) }} с.
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { computed, ComputedRef, defineComponent, useNuxt2Meta, useNuxtApp } from '#app'
import { useCursorPagination, useDebounceSearch, useFilters, useI18n, useQueryRelay } from '~/composables'
import { LogRequestsQuery, LogRequestsQueryVariables, LogRequestType, UserType } from '~/types/graphql'
import logRequestsQuery from '~/gql/core/queries/log_request.graphql'

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { $store } = useNuxtApp()
    const { t } = useI18n()
    const { dateTimeHM } = useFilters()
    useNuxt2Meta({ title: t('profile.history.name') as string })

    const user: ComputedRef<UserType> = computed<UserType>(() => $store.getters['auth/user'])

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('profile.history.tableHeaders.page') as string, value: 'page' },
      { text: t('profile.history.tableHeaders.browser') as string, value: 'session.browser' },
      { text: t('profile.history.tableHeaders.device') as string, value: 'session.device' },
      { text: t('profile.history.tableHeaders.os') as string, value: 'session.os' },
      { text: t('profile.history.tableHeaders.createdAt') as string, value: 'createdAt' },
      { text: t('profile.history.tableHeaders.time') as string, value: 'time' }
    ]))

    const { search, debounceSearch } = useDebounceSearch()
    const {
      loading,
      pagination: { count, totalCount },
      data: logRequests
    } = useQueryRelay<LogRequestsQuery, LogRequestsQueryVariables, LogRequestType>({
      document: logRequestsQuery,
      variables: () => ({
        userId: user.value.id,
        pageContains: debounceSearch.value
      }),
      options: { fetchPolicy: 'network-only' }
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    return { user, headers, loading, search, count, totalCount, logRequests, dateTimeHM }
  }
})
</script>
