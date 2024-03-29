<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ header }}
    template(v-if="period.canChangeDivisions")
      v-spacer
      add-period-divisions-menu(
        :add-header="addHeader"
        :add-button-text="addButtonText"
        :period="period"
        :add-divisions-update="addDivisionsUpdate"
        :add-divisions-from-file-update="addDivisionFromFileUpdate"
        :add-divisions-from-period-update="addDivisionFromPeriodUpdate"
      )
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ addButtonText }}
  v-row(align="center")
    v-col(cols="12" md="8")
      v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
    v-col.text-right.pr-5(
      cols="12"
      md="4"
    ) {{ $t('shownOf', { count: divisionsCount, totalCount: period.divisions.length }) }}
  v-card(flat)
    v-card-text
      v-data-table(
        :headers="tableHeaders"
        :items="period.divisions"
        :search="search"
        disable-pagination
        hide-default-footer
        @pagination="pagination"
      )
        template(#item.actions="{ item }")
          delete-menu(
            @confirm="deleteDivision({ periodId: period.id, divisionId: item.id })"
            :item-name="deleteItemName"
          )
            template(#default="{ on: onMenu }")
              v-tooltip(bottom)
                template(#activator="{ on: onTooltip }")
                  v-btn(v-on="{ ...onMenu, ...onTooltip }" color="error" icon)
                    v-icon mdi-delete
                span {{ $t('dcis.periods.divisions.deleteDivision.tooltip') }}
  v-bottom-sheet(v-model="activeMissing")
    v-card(style="position: relative" height="300px" flat)
      v-btn(icon absolute top right @click="activeMissing = false")
        v-icon mdi-close
      v-card-title Идентификаторы организаций, которые не удалось найти
      v-card-text
        v-list
          v-list-item(v-for="md in missingDivisions" :key="md") {{ md }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { computed, defineComponent, inject, ref } from '#app'
import { DataProxy } from 'apollo-cache'
import { DataPagination, DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import {
  PeriodType,
  PeriodQuery,
  DeleteDivisionMutation,
  DeleteDivisionMutationVariables,
  DeleteDivisionMutationPayload,
  DivisionModelType
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { UpdateType, useI18n } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import { AddDivisionsMutationResult } from '~/components/dcis/periods/AddPeriodDivisions.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import deleteDivisionMutation from '~/gql/dcis/mutations/period/delete_division.graphql'
import AddPeriodDivisionsMenu from '~/components/dcis/periods/AddPeriodDivisionsMenu.vue'
import { AddDivisionsFromFileMutationResult } from '~/components/dcis/periods/AddPeriodDivisionsFromFile.vue'
import { AddDivisionsFromPeriodMutationsResult } from '~/components/dcis/periods/AddPeriodDivisionsFromPeriod.vue'

export type DeleteDivisionMutationResult = { data?: { deleteDivision: DeleteDivisionMutationPayload } }

export default defineComponent({
  components: { AddPeriodDivisionsMenu, LeftNavigatorContainer, DeleteMenu },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const activeMissing = ref<boolean>(false)
    const missingDivisions = ref<number[]>([])

    const search = ref<string>('')
    const divisionsCount = ref<number>(props.period.divisions.length)
    const pagination = (pagination: DataPagination) => {
      divisionsCount.value = pagination.itemsLength
    }

    const header = computed<string>(() => props.period.project.contentType.model === 'department'
      ? t('dcis.periods.divisions.departmentsName') as string
      : t('dcis.periods.divisions.organizationsName') as string
    )

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: header.value,
        to: localePath({ name: 'dcis-periods-periodId-divisions' }),
        exact: true
      }
    ]))

    const addHeader = computed<string>(() => props.period.project.contentType.model === 'department'
      ? t('dcis.periods.divisions.addDivisions.departmentsHeader') as string
      : t('dcis.periods.divisions.addDivisions.organizationsHeader') as string
    )
    const addButtonText = computed<string>(() => props.period.project.contentType.model === 'department'
      ? t('dcis.periods.divisions.addDivisions.departmentsButtonText') as string
      : t('dcis.periods.divisions.addDivisions.organizationsButtonText') as string
    )

    const deleteItemName = computed<string>(() => props.period.project.contentType.model === 'department'
      ? t('dcis.periods.divisions.deleteDivision.departmentItemName') as string
      : t('dcis.periods.divisions.deleteDivision.organizationItemName') as string
    )

    const tableHeaders = computed(() => {
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

    const periodUpdate = inject<UpdateType<PeriodQuery>>('periodUpdate')

    const dataCacheResult = (dataCache, success: boolean, divisions: DivisionModelType[]) => {
      if (success) {
        dataCache.period.divisions = (
            [...dataCache.period.divisions, ...divisions] as Required<DivisionModelType>[]
        ).sort((d1: DivisionModelType, d2: DivisionModelType) => d1.name.localeCompare(d2.name))
      }
      return dataCache
    }

    const addDivisionsUpdate = (cache: DataProxy, result: AddDivisionsMutationResult) => periodUpdate(
      cache,
      result,
      (
        dataCache,
        { data: { addDivisions: { success, divisions } } }: AddDivisionsMutationResult
      ) => dataCacheResult(dataCache, success, divisions)
    )

    const addDivisionFromFileUpdate = (cache: DataProxy, result: AddDivisionsFromFileMutationResult) => periodUpdate(
      cache,
      result,
      (
        dataCache,
        { data: { addDivisionsFromFile: { success, divisions, missingDivisions: md } } }: AddDivisionsFromFileMutationResult
      ) => {
        if (md.length) {
          activeMissing.value = true
          missingDivisions.value = md
        }
        return dataCacheResult(dataCache, success, divisions)
      }
    )

    const addDivisionFromPeriodUpdate = (cache: DataProxy, result: AddDivisionsFromPeriodMutationsResult) => periodUpdate(
      cache,
      result,
      (
        dataCache, { data: { addDivisionsFromPeriod: { success, divisions } } }: AddDivisionsFromPeriodMutationsResult
      ) => dataCacheResult(dataCache, success, divisions)
    )

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
      activeMissing,
      missingDivisions,
      search,
      divisionsCount,
      pagination,
      header,
      bc,
      addHeader,
      addButtonText,
      deleteItemName,
      tableHeaders,
      addDivisionsUpdate,
      addDivisionFromFileUpdate,
      addDivisionFromPeriodUpdate,
      deleteDivision
    }
  }
})
</script>
