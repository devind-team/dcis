<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.groups.copyGroups.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.groups.copyGroups.buttonText'))"
  :mutation="copyPeriodGroupsMutation"
  :variables="variables"
  :update="copyPeriodGroupsUpdate"
  mutation-name="copyPeriodGroups"
  errors-in-alert
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.groups.copyGroups.period'))"
      rules="required"
    )
      v-autocomplete(
        v-model="selectedPeriod"
        :label="$t('dcis.periods.groups.copyGroups.period')"
        :items="periodItems"
        :loading="loading"
        :error-messages="errors"
        :success="valid"
        item-value="id"
        item-text="name"
        return-object
        hide-selected
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.groups.copyGroups.groups'))"
      rules="required"
    )
      v-autocomplete(
        v-model="selectedGroupIds"
        :label="$t('dcis.periods.groups.copyGroups.groups')"
        :items="selectedPeriod ? periods.find(e => e.id === selectedPeriod.id).periodGroups : []"
        :loading="loading"
        :disabled="!selectedPeriod"
        :error-messages="errors"
        :success="valid"
        item-value="id"
        item-text="name"
        chips
        deletable-chips
        multiple
        hide-selected
      )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { computed, defineComponent, PropType, ref } from '#app'
import copyPeriodGroupsMutation from '~/gql/dcis/mutations/period/copy_period_groups.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import {
  PeriodType,
  PeriodsQuery,
  PeriodsQueryVariables,
  CopyPeriodGroupsMutationVariables,
  CopyPeriodGroupsMutationPayload
} from '~/types/graphql'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'
import { useCommonQuery } from '~/composables'

export type CopyPeriodGroupsMutationResult = { data: { copyPeriodGroups: CopyPeriodGroupsMutationPayload } }
type UpdateFunction = (cache: DataProxy, result: CopyPeriodGroupsMutationResult) => DataProxy

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { data: periods, loading } = useCommonQuery<PeriodsQuery, PeriodsQueryVariables>({
      document: periodsQuery,
      variables: () => ({
        projectId: props.period.project.id
      })
    })

    const periodItems = computed<PeriodsQuery['periods']>(() => periods.value
      ? periods.value.filter(period => period.id !== props.period.id)
      : []
    )

    const selectedPeriod = ref<PeriodType | null>(null)
    const selectedGroupIds = ref<string[] | null>(null)

    const variables = computed<CopyPeriodGroupsMutationVariables>(() => ({
      periodId: props.period.id,
      selectedPeriodId: selectedPeriod.value?.id,
      periodGroupIds: selectedGroupIds.value
    }))

    /**
     * Обновление после копирования групп
     * @param cache
     * @param result
     */
    const copyPeriodGroupsUpdate = (cache: DataProxy, result: CopyPeriodGroupsMutationResult) => {
      if (result.data.copyPeriodGroups.success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      selectedPeriod.value = null
      selectedGroupIds.value = null
    }

    return {
      periods,
      loading,
      periodItems,
      copyPeriodGroupsMutation,
      selectedPeriod,
      selectedGroupIds,
      variables,
      copyPeriodGroupsUpdate,
      close
    }
  }
})
</script>
