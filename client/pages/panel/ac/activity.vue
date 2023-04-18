<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')" fluid)
  template(#header) {{ $t('profile.activity.name') }}
  v-row(align="center")
    v-col(cols="12" md="8")
      v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
    v-col.text-right.pr-5(cols="12" md="4") {{ $t('panel.ac.activity.shownOf', { count, totalCount }) }}
  v-data-table(
    :headers="headers"
    :items="logEntry"
    :loading="loading"
    dense disable-pagination hide-default-footer disable-filtering)
    template(v-slot:item.user="{ item }") {{ item.session.user.lastName }} {{ item.session.user.firstName }} {{ item.session.user.sirName }}
    template(v-slot:item.action="{ item }") {{ $t('panel.ac.activity.record') }} {{ action[item.action] }}
    template(v-slot:item.contentType="{ item }") {{ item.contentType.appLabel }}.{{ item.contentType.model }}
    template(v-slot:item.session="{ item }") {{ item.session.os }}/{{ item.session.browser }}
    template(v-slot:item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
    template(v-slot:item.info="{ item }")
      v-menu(bottom)
        template(v-slot:activator="{ on }")
          v-btn(v-on="on" icon)
            v-icon mdi-information-outline
        v-card
          v-card-text #[pre {{ parseFromJson(item.payload) }}]
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import type { PropType, ComputedRef } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useCursorPagination, useDebounceSearch, useFilters, useI18n, useQueryRelay } from '~/composables'
import { LogEntryGeneralQuery, LogEntryGeneralQueryVariables } from '~/types/graphql'
import logEntryGeneralQuery from '~/gql/core/queries/log_entry_general.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  permissions: 'devind_core.view_logentry',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { dateTimeHM } = useFilters()
    type ActionType = { A_1: string, A_2: string, A_3: string }

    const logEntryHeaders = (t: any): DataTableHeader[] => ([
      { text: t('profile.activity.tableHeaders.action') as string, value: 'action' },
      { text: t('profile.activity.tableHeaders.contentType') as string, value: 'contentType' },
      { text: t('profile.activity.tableHeaders.objectId') as string, value: 'objectId', align: 'center' },
      { text: t('profile.activity.tableHeaders.session') as string, value: 'session' },
      { text: t('profile.activity.tableHeaders.createdAt') as string, value: 'createdAt' },
      { text: t('profile.activity.tableHeaders.info') as string, value: 'info', align: 'center', width: 150 }
    ])

    const logEntryActions = (t: any): ActionType => ({
      A_1: t('profile.activity.actions.created') as string,
      A_2: t('profile.activity.actions.changed') as string,
      A_3: t('profile.activity.actions.deleted') as string
    })
    useNuxt2Meta({ title: t('profile.activity.name') as string })
    const { search, debounceSearch } = useDebounceSearch()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('profile.activity.name') as string, to: localePath({ name: 'panel-ac-activity' }), exact: true }
    ]))
    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('panel.ac.activity.tableHeaders.user') as string, value: 'user' },
      ...logEntryHeaders(t)
    ]))
    const action: ComputedRef<ActionType> = computed<ActionType>(() => (logEntryActions(t)))

    const {
      loading,
      pagination: { count, totalCount },
      data: logEntry
    } = useQueryRelay<LogEntryGeneralQuery, LogEntryGeneralQueryVariables>({
      document: logEntryGeneralQuery,
      variables: () => ({
        modelContains: debounceSearch.value
      }),
      options: { fetchPolicy: 'network-only' }
    }, {
      isScrollDown: true,
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    const parseFromJson = (text: string): Object => JSON.parse(text)

    return { bc, headers, action, search, loading, count, totalCount, logEntry, dateTimeHM, parseFromJson }
  }
})
</script>
