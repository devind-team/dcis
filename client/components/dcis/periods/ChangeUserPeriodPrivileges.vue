<template lang="pug">
mutation-modal-form(
  ref="form"
  :header="String($t('dcis.periods.users.changePrivileges.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.users.changePrivileges.buttonText'))"
  :mutation="changeUserPeriodPrivilegesMutation"
  :variables="variables"
  :update="update"
  mutation-name="changeUserPeriodPrivileges"
  errors-in-alert
  @first-activated="firstActivated"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    v-data-table(
      v-model="privileges"
      :headers="headers"
      :items="allPrivileges"
      :loading="loading"
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
  UserFieldsFragment,
  PrivilegesFieldsFragment,
  PrivilegesQuery,
  PrivilegesQueryVariables,
  UserPeriodPrivilegesQuery,
  UserPeriodPrivilegesQueryVariables,
  ChangeUserPeriodPrivilegesMutationVariables,
  ChangeUserPeriodPrivilegesMutationPayload
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import userPeriodPrivilegesQuery from '~/gql/dcis/queries/user_period_privileges.graphql'
import changeUserPeriodPrivilegesMutation from '~/gql/dcis/mutations/period/change_user_period_privilges.graphql'

type ChangeUserPeriodPrivilegesMutationResult = {
  data: { changeUserPeriodPrivileges: ChangeUserPeriodPrivilegesMutationPayload }
}

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    user: { type: Object as PropType<UserFieldsFragment>, required: true }
  },
  setup (props) {
    const firstActivated = () => {
      options.value.enabled = true
    }

    const { t } = useI18n()

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.users.changePrivileges.tableHeaders.name') as string, value: 'name' }
    ]

    const options = ref<{ enabled: boolean }>({ enabled: false })
    const { data: allPrivileges, loading: allPrivilegesLoading } = useCommonQuery<
      PrivilegesQuery,
      PrivilegesQueryVariables
    >({
      document: privilegesQuery,
      options
    })
    const {
      data: userPeriodPrivileges,
      loading: userPeriodPrivilegesLoading,
      update: userPeriodPrivilegesUpdate
    } = useCommonQuery<
      UserPeriodPrivilegesQuery,
      UserPeriodPrivilegesQueryVariables
    >({
      document: userPeriodPrivilegesQuery,
      variables: () => ({
        periodId: props.period.id,
        userId: props.user.id
      }),
      options
    })
    const loading = computed<boolean>(() => allPrivilegesLoading.value || userPeriodPrivilegesLoading.value)

    const privileges = ref<PrivilegesFieldsFragment[]>([])
    watch(userPeriodPrivileges, (value: PrivilegesFieldsFragment[]) => {
      privileges.value = value
    })

    const variables = computed<ChangeUserPeriodPrivilegesMutationVariables>(() => ({
      userId: props.user.id,
      periodId: props.period.id,
      privilegesIds: privileges.value.map((privilege: PrivilegesFieldsFragment) => privilege.id)
    }))

    const update = (
      cache: DataProxy,
      result: ChangeUserPeriodPrivilegesMutationResult
    ) => {
      if (result.data.changeUserPeriodPrivileges.success) {
        userPeriodPrivilegesUpdate(
          cache,
          result,
          (
            dataCache,
            { data: { changeUserPeriodPrivileges: { success, privileges } } }: ChangeUserPeriodPrivilegesMutationResult
          ) => {
            if (success) {
              dataCache.userPeriodPrivileges = privileges as PrivilegesFieldsFragment[]
            }
            return dataCache
          }
        )
      }
      return cache
    }

    const close = () => {
      privileges.value = [...userPeriodPrivileges.value]
    }

    return {
      firstActivated,
      changeUserPeriodPrivilegesMutation,
      headers,
      allPrivileges,
      loading,
      privileges,
      variables,
      update,
      close
    }
  }
})
</script>
