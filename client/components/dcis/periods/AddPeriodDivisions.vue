<template lang="pug">
mutation-modal-form(
  ref="form"
  :header="header"
  :subheader="period.name"
  :button-text="buttonText"
  :mutation="addDivisionsMutation"
  :variables="{ periodId: period.id, divisionIds: selectedDivisions.map(e => e.id) }"
  :update="addDivisionsUpdate"
  width="50vw"
  mutation-name="addDivisions"
  errors-in-alert
  @active-changed="activeChanged"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
    v-data-table(
      v-model="selectedDivisions"
      :headers="headers"
      :items="divisions"
      :loading="divisionsLoading"
      item-key="id"
      show-select
      disable-pagination
      hide-default-footer
    )
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { UseQueryOptions, VariablesParameter } from '@vue/apollo-composable/dist/useQuery'
import { DataProxy } from 'apollo-cache'
import { defineComponent, PropType, ref } from '#app'
import {
  DivisionModelType,
  PeriodType,
  PeriodPossibleDivisionsQuery,
  PeriodPossibleDivisionsQueryVariables,
  AddDivisionsMutationPayload
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useDebounceSearch, useI18n } from '~/composables'
import periodPossibleDivisionsQuery from '~/gql/dcis/queries/period_possible_divisions.graphql'
import addDivisionsMutation from '~/gql/dcis/mutations/period/add_divisions.graphql'

export type AddDivisionsMutationResult = { data: { addDivisions: AddDivisionsMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddDivisionsMutationResult | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    header: { type: String, required: true },
    buttonText: { type: String, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const activeChanged = (active: boolean) => {
      if (active) {
        queryOptions.value.enabled = true
        refetchDivisions()
      } else {
        queryOptions.value.enabled = false
      }
    }

    const queryOptions = ref<UseQueryOptions<
      PeriodPossibleDivisionsQuery,
      PeriodPossibleDivisionsQueryVariables
    >>({ enabled: false, fetchPolicy: 'no-cache' })
    const { search, debounceSearch } = useDebounceSearch()
    const { data: divisions, loading: divisionsLoading, refetch: refetchDivisions } = useQueryRelay<
      PeriodPossibleDivisionsQuery,
      PeriodPossibleDivisionsQueryVariables,
      DivisionModelType
    >({
      document: periodPossibleDivisionsQuery,
      options: queryOptions,
      variables: () => {
        const result: VariablesParameter<PeriodPossibleDivisionsQueryVariables> = {
          periodId: props.period.id,
          search: debounceSearch.value
        }
        if (debounceSearch.value) {
          result.first = 100
        }
        return result
      }
    })

    const selectedDivisions = ref<DivisionModelType[]>([])

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.addDivisions.name') as string, value: 'name' }
    ]

    const addDivisionsUpdate = (cache: DataProxy, result: AddDivisionsMutationResult) => {
      if (result.data.addDivisions.success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      selectedDivisions.value = []
      search.value = ''
      emit('close')
    }

    return {
      activeChanged,
      addDivisionsMutation,
      search,
      divisions,
      divisionsLoading,
      selectedDivisions,
      headers,
      addDivisionsUpdate,
      close
    }
  }
})
</script>
