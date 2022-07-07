<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.divisions.addDivisions.header'))"
    :button-text="String($t('dcis.periods.divisions.addDivisions.buttonText'))"
    :mutation="addDivisions"
    :update="addDivisionsUpdate"
    :variables="{ periodId: period.id, divisionIds: selectedDivisions.map(e => e.id) }"
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
        :items-per-page="33"
        :search.sync="search"
        item-key="id"
        show-select
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
import addDivisions from '~/gql/dcis/mutations/project/add_divisions.graphql'

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

    return { addDivisions, search, selectedDivisions, headers, addDivisionsUpdate, close }
  }
})
</script>
