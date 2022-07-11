<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.users.changeGroups.header'))"
    :subheader="period.name"
    :button-text="String($t('dcis.periods.users.changeGroups.buttonText'))"
    :mutation="changeUserPeriodGroupsMutation"
    :variables="variables"
    :update="update"
    mutation-name="changeUserPeriodGroups"
    errors-in-alert
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-data-table(
        v-model="userGroups"
        :headers="headers"
        :items="period.periodGroups"
        item-key="id"
        show-select
        disable-pagination
        hide-default-footer
      )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import type { PropType } from '#app'
import {
  PeriodType,
  PeriodGroupType,
  UserType,
  UserFieldsFragment,
  ChangeUserPeriodGroupsMutationVariables,
  ChangeUserPeriodGroupsMutationPayload
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import changeUserPeriodGroupsMutation from '~/gql/dcis/mutations/period/change_user_period_groups.graphql'

export type ChangeUserPeriodGroupsMutationResult = {
  data: { changeUserPeriodGroups: Required<ChangeUserPeriodGroupsMutationPayload> }
}
type UpdateFunction = (cache: DataProxy, result: ChangeUserPeriodGroupsMutationResult) => DataProxy

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    user: { type: Object as PropType<UserFieldsFragment>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.users.changeGroups.tableHeaders.name') as string, value: 'name' }
    ]

    const getUserGroups = () => {
      return props.period.periodGroups.filter((periodGroup: PeriodGroupType) =>
        periodGroup.users.find((user: UserType) => user.id === props.user.id)
      )
    }
    const userGroups = ref<PeriodGroupType[]>(getUserGroups())
    const close = () => {
      userGroups.value = getUserGroups()
    }

    const variables = computed<ChangeUserPeriodGroupsMutationVariables>(() => ({
      userId: props.user.id,
      periodGroupIds: userGroups.value.map((periodGroup: PeriodGroupType) => periodGroup.id)
    }))

    return { changeUserPeriodGroupsMutation, headers, userGroups, close, variables }
  }
})
</script>
