<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.divisions.addDivisions.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.divisions.addDivisions.buttonText'))"
  :mutation="addDivisionsMutation"
  :variables="{ periodId: period.id, divisionIds: selectedDivisions.map(e => e.id) }"
  :update="addDivisionsUpdate"
  width="50vw"
  mutation-name="addDivisions"
  errors-in-alert
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
      :loading="loading"
      :search="search"
      item-key="id"
      show-select
      disable-pagination
      hide-default-footer
    )
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import { DataProxy } from 'apollo-cache'
import {
  DivisionModelType,
  PeriodType,
  AddDivisionsMutationPayload
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useDebounceSearch, useI18n } from '~/composables'
import addDivisionsMutation from '~/gql/dcis/mutations/period/add_divisions.graphql'

export type ChangeDivisionsMutationResult = { data: { addDivisions: AddDivisionsMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddDivisionsMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    divisions: { type: Array as PropType<DivisionModelType[]>, default: () => [] },
    loading: { type: Boolean as PropType<boolean>, default: false },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { search } = useDebounceSearch()

    const selectedDivisions = ref<DivisionModelType[]>([])

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.addDivisions.name') as string, value: 'name' }
    ]

    const addDivisionsUpdate = (cache: DataProxy, result: ChangeDivisionsMutationResult) => {
      if (result.data.addDivisions.success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      selectedDivisions.value = []
      search.value = ''
    }

    return { addDivisionsMutation, search, selectedDivisions, headers, addDivisionsUpdate, close }
  }
})
</script>