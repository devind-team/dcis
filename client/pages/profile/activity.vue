<template lang="pug">
  v-card
    v-card-title {{ $t('profile.activity.name') }}
      v-spacer
      .caption {{ $t('shownOf', { count, totalCount }) }}
    v-card-text
      v-row
        v-col
          v-data-table(
            :headers="headers"
            :items="logEntry"
            :loading="loading"
            dense disable-pagination hide-default-footer)
            template(v-slot:item.action="{ item }") {{ $t('profile.activity.record') }} {{ action[item.action] }}
            template(v-slot:item.contentType="{ item }") {{ item.contentType.appLabel }}.{{ item.contentType.model }}
            template(v-slot:item.session="{ item }") {{ item.session.os }}/{{ item.session.browser }}
            template(v-slot:item.createdAt="{ item }") {{ $filters.dateTimeHM(item.createdAt) }}
            template(v-slot:item.info="{ item }")
              v-menu(bottom)
                template(v-slot:activator="{ on }")
                  v-btn(v-on="on" icon)
                    v-icon mdi-information-outline
                v-card
                  v-card-text #[pre {{ parseFromJson(item.payload) }}]
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify/types'
import { computed, defineComponent, Ref, toRef, useNuxt2Meta } from '#app'
import type { ComputedRef } from '#app'
import type { LogEntryQuery, LogEntryQueryVariables, LogEntryType, UserType } from '~/types/graphql'
import { useAuthStore } from '~/store'
import { useCursorPagination, useI18n, useQueryRelay } from '~/composables'
import logEntryQuery from '~/gql/core/queries/log_entry.graphql'

export type ActionType = { A_1: string, A_2: string, A_3: string }

export const logEntryHeaders = (t: any): DataTableHeader[] => ([
  { text: t('profile.activity.tableHeaders.action') as string, value: 'action' },
  { text: t('profile.activity.tableHeaders.contentType') as string, value: 'contentType' },
  { text: t('profile.activity.tableHeaders.objectId') as string, value: 'objectId', align: 'center' },
  { text: t('profile.activity.tableHeaders.session') as string, value: 'session' },
  { text: t('profile.activity.tableHeaders.createdAt') as string, value: 'createdAt' },
  { text: t('profile.activity.tableHeaders.info') as string, value: 'info', align: 'center', width: 150 }
])

export const logEntryActions = (t: any): ActionType => ({
  A_1: t('profile.activity.actions.created') as string,
  A_2: t('profile.activity.actions.changed') as string,
  A_3: t('profile.activity.actions.deleted') as string
})

export default defineComponent({
  middleware: 'auth',
  setup () {
    const { t } = useI18n()
    const userStore = useAuthStore()

    useNuxt2Meta({ title: t('profile.activity.name') as string })

    const user: Ref<UserType> = toRef(userStore, 'user')
    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => (logEntryHeaders(t)))
    const action: ComputedRef<ActionType> = computed<ActionType>(() => (logEntryActions(t)))

    const parseFromJson = (text: string): Object => JSON.parse(text)

    const {
      loading,
      pagination: { count, totalCount },
      data: logEntry
    } = useQueryRelay<LogEntryQuery, LogEntryQueryVariables, LogEntryType>({
      document: logEntryQuery,
      variables: () => ({
        userId: user.value.id
      })
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    return {
      t,
      loading,
      headers,
      action,
      count,
      totalCount,
      logEntry,
      parseFromJson
    }
  }
})
</script>
