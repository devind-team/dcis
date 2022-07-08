<template lang="pug">
  v-data-table(
    v-model="privileges"
    :key="group.id"
    :headers="headers"
    :items="allPrivileges"
    :loading="loading"
    :show-select="canChange"
    hide-default-footer
  )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify'
import { PropType } from '#app'
import {
  PeriodGroupType,
  PrivilegeType,
  PrivilegesQuery,
  PrivilegesQueryVariables,
  ChangePeriodGroupPrivilegesMutation,
  ChangePeriodGroupPrivilegesMutationPayload,
  ChangePeriodGroupPrivilegesMutationVariables
} from '~/types/graphql'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import changePeriodGroupPrivilegesMutation from '~/gql/dcis/mutations/project/change_period_group_privileges.graphql'

export type ChangePeriodGroupPrivilegesMutationResult = {
  data?: { changePeriodGroupPrivileges: ChangePeriodGroupPrivilegesMutationPayload }
}
type UpdateFunction = (
  cache: DataProxy | any,
  result: ChangePeriodGroupPrivilegesMutationResult
) => DataProxy

export default defineComponent({
  props: {
    group: { type: Object as PropType<PeriodGroupType>, required: true },
    canChange: { type: Boolean, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.groups.privileges.tableHeaders.name') as string, value: 'name' },
      { text: t('dcis.periods.groups.privileges.tableHeaders.key') as string, value: 'key' }
    ]

    const { data: allPrivileges, loading: privilegesLoading } = useCommonQuery<
      PrivilegesQuery,
      PrivilegesQueryVariables
    >({
      document: privilegesQuery
    })

    const { mutate: changePrivileges, loading: changePrivilegesLoading } = useMutation<
      ChangePeriodGroupPrivilegesMutation,
      ChangePeriodGroupPrivilegesMutationVariables
    >(
      changePeriodGroupPrivilegesMutation, {
        update: props.update
      }
    )

    const privileges = computed<PrivilegeType[]>({
      get () {
        if (!allPrivileges.value) {
          return []
        }
        return allPrivileges.value.filter((privilege: PrivilegeType) =>
          props.group.privileges.find((groupPrivilege: PrivilegeType) => privilege.id === groupPrivilege.id))
      },
      async set (value: PrivilegeType[]) {
        await changePrivileges({
          periodGroupId: props.group.id,
          privilegesIds: value.map((privilege: PrivilegeType) => privilege.id)
        })
      }
    })

    const loading = computed<boolean>(() => privilegesLoading.value || changePrivilegesLoading.value)

    return { headers, allPrivileges, changePrivileges, privileges, loading }
  }
})
</script>
