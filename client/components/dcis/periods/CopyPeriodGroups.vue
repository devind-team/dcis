<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.copyPeriodGroups.header'))"
    :button-text="String($t('dcis.periods.copyPeriodGroups.buttonText'))"
    :mutation="copyPeriodGroups"
    :variables="{ periodId: selectPeriod }"
    mutation-name="copyPeriodGroups"
    errors-in-alert
    persistent
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-autocomplete(
        v-model="selectPeriod"
        :label="String($t('dcis.periods.copyPeriodGroups.period'))"
        :items="periods"
        :loading="loading"
        item-text="name"
        item-value="id"
        return-object
        hide-no-data
        hide-selected
      )
      v-autocomplete(
        v-model="selectGroups"
        :label="String($t('dcis.periods.copyPeriodGroups.groups'))"
        :items="selectPeriod ? periods.find(e => e.id === selectPeriod.id).periodGroups: []"
        :loading="loading"
        :disabled="!selectPeriod"
        item-text="name"
        item-value="id"
        return-object
        hide-no-data
        hide-selected
      )
</template>

<script lang="ts">
import { defineComponent } from '#app'
import copyPeriodGroups from '~/gql/dcis/mutations/project/copy_period_groups.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { PeriodType, PeriodsQuery, PeriodsQueryVariables, PeriodGroupType } from '~/types/graphql'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'
import { useAuthStore } from '~/store'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    activeQuery: { type: Boolean, default: false }
  },
  setup (props) {
    const authStore = useAuthStore()

    const user = toRef(authStore, 'user')
    const selectPeriod = ref<PeriodType | null>(null)
    const selectGroups = ref<PeriodGroupType[] | null>(null)

    const options = ref({ enabled: props.activeQuery })
    const { data: periods, loading } = useCommonQuery<PeriodsQuery, PeriodsQueryVariables>({
      document: periodsQuery,
      variables: () => ({
        userId: user.value.id
      }),
      options: options.value
    })
    return {
      selectPeriod,
      selectGroups,
      periods,
      loading,
      copyPeriodGroups
    }
  }
})
</script>
