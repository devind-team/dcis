<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) {{ $t('dcis.periods.divisions.name') }}
      template(v-if="period.canChangeDivisions")
        v-spacer
        add-divisions(
          :period="period"
          :divisions="filterDivisions"
          :loading="loading"
          :update="addDivisionsUpdate"
        )
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") {{ $t('dcis.periods.divisions.addDivisions.buttonText') }}
    v-row(align="center")
      v-col(cols="12" md="8")
        v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right.pr-5(
        cols="12"
        md="4"
      ) {{ $t('dcis.periods.divisions.shownOf', { count: period.divisions.length }) }}
    v-card(flat)
      v-card-text
        v-data-table(
          :headers="headers"
          :items="period.divisions"
          :search.sync="search"
          :loading="loading"
          disable-pagination
          hide-default-footer
        )
          template(#item.actions="{ item }")
            delete-menu(
              :item-name="String($t('dcis.periods.divisions.deleteDivision.itemName'))"
              @confirm="deleteDivision({ periodId: period.id, divisionId: item.id })"
            )
              template(#default="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{ ...onMenu, ...onTooltip }" color="error" icon)
                      v-icon mdi-delete
                  span {{ $t('dcis.periods.divisions.deleteDivision.tooltip') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { computed, defineComponent, inject } from '#app'
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import {
  PeriodType,
  PeriodQuery,
  DeleteDivisionMutation,
  DeleteDivisionMutationVariables,
  DeleteDivisionMutationPayload,
  ProjectDivisionsQuery,
  ProjectDivisionsQueryVariables, DivisionModelType
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { UpdateType, useCommonQuery, useDebounceSearch, useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AddDivisions, { ChangeDivisionsMutationResult } from '~/components/dcis/periods/AddDivisions.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import divisionsQuery from '~/gql/dcis/queries/project_divisions.graphql'
import deleteDivisionMutation from '~/gql/dcis/mutations/project/delete_division.graphql'

export type DeleteDivisionMutationResult = { data?: { deleteDivision: DeleteDivisionMutationPayload } }

export default defineComponent({
  components: { LeftNavigatorContainer, AddDivisions, DeleteMenu },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { search } = useDebounceSearch()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.divisions.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-divisions' }),
        exact: true
      }
    ]))

    const headers = computed(() => {
      const result: DataTableHeader[] = [
        {
          text: t('dcis.periods.divisions.tableHeaders.name') as string,
          value: 'name'
        }
      ]
      if (props.period.canChangeDivisions) {
        result.push({
          text: t('dcis.periods.divisions.tableHeaders.actions') as string,
          value: 'actions',
          align: 'center',
          sortable: false,
          filterable: false
        })
      }
      return result
    })

    const { data: projectDivisions, loading } = useCommonQuery<
      ProjectDivisionsQuery,
      ProjectDivisionsQueryVariables
    >({
      document: divisionsQuery,
      variables: { projectId: props.period.project.id }
    })

    const filterDivisions = computed<DivisionModelType[]>(() => {
      if (projectDivisions.value) {
        return projectDivisions.value.filter(division =>
          !props.period.divisions.map(periodDivision => periodDivision.id).includes(division.id))
      }
      return []
    })

    const periodUpdate: UpdateType<PeriodQuery> = inject('periodUpdate')

    const addDivisionsUpdate = (cache: DataProxy, result: ChangeDivisionsMutationResult) => periodUpdate(
      cache,
      result,
      (dataCache, { data: { addDivisions: { success, divisions } } }: ChangeDivisionsMutationResult) => {
        if (success) {
          dataCache.period.divisions = (
            [...dataCache.period.divisions, ...divisions] as Required<DivisionModelType>[]
          ).sort((d1: DivisionModelType, d2: DivisionModelType) => d1.name.localeCompare(d2.name))
        }
        return dataCache
      })

    const { mutate: deleteDivision } = useMutation<
      DeleteDivisionMutation,
      DeleteDivisionMutationVariables
    >(
      deleteDivisionMutation,
      {
        update: (cache, result) => periodUpdate(
          cache,
          result,
          (dataCache, { data: { deleteDivision: { success, deleteId } } }: DeleteDivisionMutationResult) => {
            if (success) {
              dataCache.period.divisions = dataCache.period.divisions
                .filter((division: DivisionModelType) => String(division.id) !== deleteId)
            }
            return dataCache
          }
        )
      })

    return {
      search,
      bc,
      headers,
      loading,
      filterDivisions,
      addDivisionsUpdate,
      deleteDivision
    }
  }
})
</script>
