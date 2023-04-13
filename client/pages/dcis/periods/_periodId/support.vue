<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.links.support') }}
  v-card-text
    v-row(align="center")
      v-col(cols="12")
        v-btn(v-if="period.isAdmin || period.isCurator || period.canChangePeriodMethodicalSupport" @click="addFilesHandle" color="primary")
          v-icon(left) mdi-upload
          | {{ $t('dcis.periods.methodical_support.uploadFiles') }}
    v-row
      v-col(cols="12" sm="6")
        v-text-field(v-model="search" :label="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right(cols="12" sm="6") {{ $t('dcis.periods.methodical_support.shownOf', { count, totalCount }) }}
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
            v-tooltip(bottom)
              template(#activator="{ on: onTooltip }")
                a(v-on="{...onTooltip}" :href="`/${item.src}`" target="__blank") {{ item.name }}
              span {{ $t('dcis.periods.methodical_support.downloadFile') }}
          template(#item.updated="{ item }") {{ $filters.dateTimeHM(item.updatedAt) }}
          template(#item.size="{ item }") {{ (item.size / 1024).toFixed(2) }} {{ $t('dcis.periods.methodical_support.kB') }}
          template(#item.actions="{ item }")
            template(v-if="period.isAdmin || period.isCurator || period.canChangePeriodMethodicalSupport")
              text-menu(v-slot="{ on: onMenu }" :value="item.name" @update="changePeriodMethodicalSupportMutate({ fileId: item.id, field: 'name', value: $event }).then()")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{ ...onMenu, ...onTooltip }" icon color="primary")
                      v-icon mdi-pencil
                  span {{ $t('dcis.periods.methodical_support.changeName') }}
              delete-menu(
                v-slot="{ on: onMenu }"
                :item-name="String($t('dcis.periods.methodical_support.file'))"
                @confirm="deletePeriodMethodicalSupportMutate({ fileId: item.id }).then()" color="error"
              )
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{ ...onMenu, ...onTooltip }" icon color="error")
                      v-icon mdi-delete
                  span {{ $t('dcis.periods.methodical_support.deleteFile') }}
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

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => {
      const result = [
        { text: t('dcis.periods.methodical_support.tableHeaders.name') as string, value: 'name', sortable: false },
        { text: t('dcis.periods.methodical_support.tableHeaders.ext') as string, value: 'ext', sortable: false, width: 120 },
        { text: t('dcis.periods.methodical_support.tableHeaders.updated') as string, value: 'updated', sortable: false },
        { text: t('dcis.periods.methodical_support.tableHeaders.size') as string, value: 'size', sortable: false, width: 120 }
      ]
      if (props.period.isAdmin || props.period.isCurator || props.period.canChangePeriodMethodicalSupport) {
        result.push({ text: t('dcis.periods.methodical_support.tableHeaders.actions') as string, value: 'actions', sortable: false, width: 150 })
      }
      return result
    })

    const { mutate: addPeriodMethodicalSupportMutate } = useMutation<
      AddPeriodMethodicalSupportMutation,
      AddPeriodMethodicalSupportMutationVariables
    >(
      addPeriodMethodicalSupport,
      {
        update: (cache, result) => {
          if (!result.data.addPeriodMethodicalSupport.errors.length) {
            addUpdate(cache, result)
          }
        }
      }
    )

    const { select: addFilesHandle } = useSelectFiles((file: FileList) => {
      addPeriodMethodicalSupportMutate({ periodId: props.period.id, files: file })
    })

    const { mutate: changePeriodMethodicalSupportMutate } = useMutation<ChangePeriodMethodicalSupportMutation, ChangePeriodMethodicalSupportMutationVariables>(changePeriodMethodicalSupport, {
      update: (cache, result) => {
        if (!result.data.changePeriodMethodicalSupport.success) {
          changeUpdate(cache, result)
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
