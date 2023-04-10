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
          template(#item.name="{ item }")
            a(:href="`/${item.src}`" target="__blank") {{ item.name }}
          template(#item.updated="{ item }") {{ $filters.dateTimeHM(item.updatedAt) }}
          template(#item.size="{ item }") {{ (item.size / 1024).toFixed(2) }} {{ $t('profile.files.kB') }}
          template(#item.actions="{ item }")
            text-menu(v-slot="{ on: onMenu }" :value="item.name" @update="changePeriodMethodicalSupportMutate({ fileId: item.id, field: 'name', value: $event }).then()")
              v-tooltip(bottom)
                template(#activator="{ on: onTooltip }")
                  v-btn(v-on="{...onMenu, ...onTooltip}" icon color="primary")
                    v-icon mdi-pencil
                span {{ $t('profile.files.changeName') }}
            delete-menu(
              v-slot="{ on: onMenu }"
              :item-name="String($t('profile.files.file'))"
              @confirm="deletePeriodMethodicalSupportMutate({ fileId: item.id, periodId: period.id }).then()" color="error"
            )
              v-tooltip(bottom)
                template(#activator="{ on: onTooltip }")
                  v-list-item-action(v-on="{ ...onMenu, ...onTooltip }")
                    v-btn(color="error" icon)
                      v-icon mdi-delete
                span {{ $t('profile.files.deleteFile') }}
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
  AddPeriodMethodicalSupportMutation,
  AddPeriodMethodicalSupportMutationVariables,
  ChangePeriodMethodicalSupportMutation,
  ChangePeriodMethodicalSupportMutationVariables,
  DeletePeriodMethodicalSupportMutation,
  DeletePeriodMethodicalSupportMutationVariables,
  PeriodMethodicalSupportQuery,
  PeriodMethodicalSupportQueryVariables,
  PeriodType,
  UserType
} from '~/types/graphql'
import periodMethodicalSupportQuery from '~/gql/dcis/queries/period_methodical_support.graphql'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import addPeriodMethodicalSupport from '~/gql/dcis/mutations/period/add_period_methodical_support.graphql'
import changePeriodMethodicalSupport from '~/gql/dcis/mutations/period/change_period_methodical_support.graphql'
import deletePeriodMethodicalSupportMutation from '~/gql/dcis/mutations/period/delete_period_methodical_support.graphql'
import TextMenu from '~/components/common/menu/TextMenu.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export default defineComponent({
  components: { DeleteMenu, TextMenu, LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const authStore = useAuthStore()
    const { hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

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
    } = useQueryRelay<PeriodMethodicalSupportQuery, PeriodMethodicalSupportQueryVariables>({
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

    const { mutate: addPeriodMethodicalSupportMutate } = useMutation<
      AddPeriodMethodicalSupportMutation,
      AddPeriodMethodicalSupportMutationVariables
    >(
      addPeriodMethodicalSupport,
      {
        update: (cache, result) => {
          if (!result.data.addPeriodMethodicalSupport.errors.length) {
            addUpdate(cache, result, 'periodMethodicalSupport')
          }
        }
      }
    )
    const { select: addFilesHandle } = useSelectFiles((files: FileList) => {
      addPeriodMethodicalSupportMutate({ periodId: props.period.id, files })
    })

    const { mutate: changePeriodMethodicalSupportMutate } = useMutation<ChangePeriodMethodicalSupportMutation, ChangePeriodMethodicalSupportMutationVariables>(changePeriodMethodicalSupport, {
      update: (cache, result) => {
        if (!result.data.changePeriodMethodicalSupport.success) {
          changeUpdate(cache, result, 'periodMethodicalSupport')
        }
      }
    })
    const { mutate: deletePeriodMethodicalSupportMutate } = useMutation<DeletePeriodMethodicalSupportMutation, DeletePeriodMethodicalSupportMutationVariables>(deletePeriodMethodicalSupportMutation, {
      update: (cache, result) => {
        if (result.data.deletePeriodMethodicalSupport.success) {
          deleteUpdate(cache, result, true)
        }
      }
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
      hasPerm,
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
      addFilesHandle,
      changePeriodMethodicalSupportMutate,
      deletePeriodMethodicalSupportMutate
    }
  }
})
</script>
