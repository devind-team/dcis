<template lang="pug">
mutation-form(
  v-if="canChange"
  :button-text="String($t('dcis.periods.groups.changePrivileges.buttonText'))"
  :mutation="changePeriodGroupPrivilegesMutation"
  :variables="variables"
  :update="update"
  :show-success="false"
  mutation-name="changePeriodGroupPrivileges"
  errors-in-alert
  flat
)
  template(#form)
    v-data-table(
      v-model="privileges"
      :headers="headers"
      :items="allPrivileges"
      :loading="loading"
      show-select
      hide-default-footer
      disable-pagination
    )
v-data-table(
  v-else
  :headers="headers"
  :items="group.privileges"
  hide-default-footer
)
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { PropType } from '#app'
import {
  PeriodGroupType,
  PrivilegeType,
  PrivilegesQuery,
  PrivilegesQueryVariables,
  ChangePeriodGroupPrivilegesMutationPayload,
  ChangePeriodGroupPrivilegesMutationVariables
} from '~/types/graphql'
import MutationForm from '~/components/common/forms/MutationForm.vue'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import changePeriodGroupPrivilegesMutation from '~/gql/dcis/mutations/period/change_period_group_privileges.graphql'

export type ChangePeriodGroupPrivilegesMutationResult = {
  data?: { changePeriodGroupPrivileges: ChangePeriodGroupPrivilegesMutationPayload }
}
type UpdateFunction = (
  cache: DataProxy | any,
  result: ChangePeriodGroupPrivilegesMutationResult
) => DataProxy

export default defineComponent({
  components: { MutationForm },
  props: {
    group: { type: Object as PropType<PeriodGroupType>, required: true },
    canChange: { type: Boolean, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.groups.changePrivileges.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.periods.groups.changePrivileges.tableHeaders.key') as string, value: 'key' }
    ]

    const { data: allPrivileges, loading } = useCommonQuery<
      PrivilegesQuery,
      PrivilegesQueryVariables
    >({
      document: privilegesQuery,
      options: computed(() => ({ enabled: props.canChange }))
    })
    const getPrivileges = () => {
      if (!allPrivileges.value) {
        return []
      }
      return allPrivileges.value.filter((privilege: PrivilegeType) =>
        props.group.privileges.find((groupPrivilege: PrivilegeType) => privilege.id === groupPrivilege.id))
    }
    const privileges = ref<PrivilegeType[]>(getPrivileges())
    watch(() => props.group, () => {
      privileges.value = getPrivileges()
    })
    watch(allPrivileges, () => {
      privileges.value = getPrivileges()
    })

    const variables = computed<ChangePeriodGroupPrivilegesMutationVariables>(() => ({
      periodGroupId: props.group.id,
      privilegesIds: privileges.value.map((privilege: PrivilegeType) => privilege.id)
    }))

    return {
      changePeriodGroupPrivilegesMutation,
      headers,
      allPrivileges,
      loading,
      privileges,
      variables
    }
  }
})
</script>
