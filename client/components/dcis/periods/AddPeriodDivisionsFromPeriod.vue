<template lang="pug">
mutation-modal-form(
  :header="header"
  :subheader="period.name"
  :button-text="buttonText"
  :mutation="addPeriodDivisionsFromPeriodMutation"
  :variables="{ periodId: period.id, periodFromId}"
  :update="update"
  width="40vw"
  mutation-name="addDivisionsFromPeriod"
  errors-in-alert
  @close="$emit('close')"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(v-slot="{ error, valid }" :name="String($t('dcis.periods.choicePeriod'))" rules="required")
      v-select(
        v-model="periodFromId"
        :label="String($t('dcis.periods.choicePeriod'))"
        :loading="loading"
        :items="(periods || []).filter(p => p.id !== period.id)"
        item-text="name"
        item-value="id"
      )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, PropType, ref } from '#app'
import { AddDivisionsFromPeriodMutationPayload, PeriodType } from '~/types/graphql'
import { usePeriodsQuery } from '~/services/grapqhl/queries/dcis/periods'
import addPeriodDivisionsFromPeriodMutation from '~/gql/dcis/mutations/period/add_divisions_form_period.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddDivisionsFromPeriodMutationsResult = { data: { addDivisionsFromPeriod: AddDivisionsFromPeriodMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddDivisionsFromPeriodMutationsResult) => void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    header: { type: String, required: true },
    buttonText: { type: String, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const periodFromId = ref<number | string | null>(null)
    const { data: periods, loading } = usePeriodsQuery(props.period.project.id)
    return { periods, loading, periodFromId, addPeriodDivisionsFromPeriodMutation }
  }
})
</script>
