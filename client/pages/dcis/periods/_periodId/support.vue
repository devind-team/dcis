<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.links.support') }}
  v-card-text
    v-row(align="center")
      v-col(cols="12")
        v-btn(@click="addFilesHandle" color="primary")
          v-icon(left) mdi-upload
          | {{ $t('profile.files.downloadFiles') }}
    v-row
      v-col(cols="12" sm="6")
        v-text-field(v-model="search" :label="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right(cols="12" sm="6") {{ $t('profile.files.shownOf', { count, totalCount }) }}
    v-row
      v-col
       v-data-table(
          :headers="headers"
          :items="files"
          :loading="loading"
          disable-pagination
          hide-default-footer
        )
  pre {{ files }}
</template>
<script lang="ts">
import { defineComponent, computed, ComputedRef, PropType, toRefs } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import { BreadCrumbsItem } from '~/types/devind'
import { useCursorPagination, useDebounceSearch, useI18n, useQueryRelay, useSelectFiles } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import {
  AddFileMutation, AddFileMutationVariables,
  MethodicalSupportQuery,
  MethodicalSupportQueryVariables,
  PeriodType,
  UserType
} from '~/types/graphql'
import periodMethodicalSupportQuery from '~/gql/dcis/queries/period_methodical_support.graphql'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import addFile from '~/gql/core/mutations/file/add_file.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const authStore = useAuthStore()
    const { user } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

    const { search, debounceSearch } = useDebounceSearch({
      callback: () => setPage(1)
    })

    const {
      loading,
      pagination: { setPage, totalCount, count },
      data,
      fetchMoreAvailable,
      fetchMoreData,
      addUpdate,
      changeUpdate,
      deleteUpdate
    } = useQueryRelay<MethodicalSupportQuery, MethodicalSupportQueryVariables>({
      document: periodMethodicalSupportQuery,
      variables: () => ({
        periodId: props.period.id,
        nameContains: debounceSearch.value
      })
    }, {
      isScrollDown: true,
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('profile.files.tableHeaders.name') as string, value: 'name' },
      { text: t('profile.files.tableHeaders.ext') as string, value: 'ext', width: 120 },
      { text: t('profile.files.tableHeaders.updated') as string, value: 'updated' },
      { text: t('profile.files.tableHeaders.size') as string, value: 'size', width: 120 },
      { text: t('profile.files.tableHeaders.actions') as string, value: 'actions', sortable: false, width: 150 }
    ]))

    const { mutate: addFileMutate } = useMutation<AddFileMutation, AddFileMutationVariables>(addFile, {
      update: (cache, result) => addUpdate(cache, result)
    })
    const { select: addFilesHandle } = useSelectFiles((files: FileList) => {
      addFileMutate({ userId: user.value.id, files })
    })
    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.links.support') as string,
        to: localePath({ name: 'dcis-periods-periodId-support' }),
        exact: true
      }
    ]))
    return {
      bc,
      // hasPerm,
      headers,
      search,
      debounceSearch,
      loading,
      files: data,
      count,
      totalCount,
      fetchMoreAvailable,
      fetchMoreData,
      setPage,
      addFilesHandle
      // changeFileMutate,
      // deleteFileMutate
    }
  }
})
</script>
