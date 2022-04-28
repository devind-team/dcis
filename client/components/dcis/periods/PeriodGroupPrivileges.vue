<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.changePrivileges.header'))"
    :subheader="itemName"
    :button-text="String($t('dcis.periods.changePrivileges.buttonText'))"
    :mutation="user ? changeGroupUsersPrivileges : changePeriodGroupPrivileges"
    :update="user ? changeUsersPrivilegesUpdate : changeGroupPrivilegesUpdate"
    :variables="formVariables"
    :mutation-name="mutationName"
    errors-in-alert
    persistent
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-data-table(
        v-model="selectPrivileges"
        :headers="headers"
        :items="user ? periodGroup.privileges : privileges"
        :loading="loading"
        item-key="id"
        show-select
        hide-default-footer
      )
        template(#no-data)
          v-alert(type="warning") {{ $t('dcis.periods.changePrivileges.alert') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { computed, defineComponent, inject, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import {
  ChangeGroupUserPrivilegesMutationPayload,
  ChangePeriodGroupPrivilegesMutationPayload,
  PeriodGroupType,
  PeriodType,
  PrivilegesQuery,
  PrivilegesQueryVariables,
  PrivilegeType,
  UserType
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import {useCommonQuery, useFilters, useI18n} from '~/composables'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import changePeriodGroupPrivileges from '~/gql/dcis/mutations/privelege/change_period_group_privileges.graphql'
import changeGroupUsersPrivileges from '~/gql/dcis/mutations/privelege/change_user_privileges.graphql'

export type ChangePeriodGroupPrivilegesMutationResult = { data: { changePeriodGroupPrivileges: ChangePeriodGroupPrivilegesMutationPayload } }
export type ChangeGroupUsersPrivilegesMutationResult = { data: { changeGroupUsersPrivileges: ChangeGroupUserPrivilegesMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: ChangeGroupUserPrivilegesMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    activeQuery: { type: Boolean as PropType<boolean>, default: false },
    periodGroup: { type: Object as PropType<PeriodGroupType>, required: true },
    period: { type: Object as PropType<PeriodType>, default: null },
    user: { type: Object as PropType<UserType>, default: null },
    userPrivileges: { type: Array as PropType<PrivilegeType[]>, default: null },
    update: { type: Function as PropType<UpdateFunction>, default: () => null }
  },
  setup (props) {
    const { t } = useI18n()
    const { getUserFullName } = useFilters()

    const activeQuery = ref<boolean>(props.activeQuery)
    const options = ref({ enabled: activeQuery })
    const selectPrivileges = ref<PrivilegeType[]>(props.user ? props.userPrivileges : props.periodGroup.privileges)

    const itemName = computed<string>(() => (props.user ? getUserFullName(props.user) : props.periodGroup.name))
    const mutationName = computed<string>(() => (props.user ? 'changeGroupUsersPrivileges' : 'changePeriodGroupPrivileges'))
    const formVariables = computed<any>(() => {
      if (props.user) {
        return { periodId: props.period.id, userId: props.user.id, privilegesIds: selectPrivileges.value.map(e => e.id) }
      } else {
        return { periodGroupId: props.periodGroup.id, privilegesIds: selectPrivileges.value.map(e => e.id) }
      }
    })
    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.changePrivileges.name') as string, value: 'name' },
      { text: t('dcis.periods.changePrivileges.key') as string, value: 'key' }
    ]))
    const { data: privileges, loading } = useCommonQuery<PrivilegesQuery, PrivilegesQueryVariables>({
      document: privilegesQuery,
      options: options.value
    })
    const periodGroupPrivilegesUpdate: any = inject('periodGroupPrivilegesUpdate')
    const changeGroupPrivilegesUpdate = (cache: DataProxy, result: ChangePeriodGroupPrivilegesMutationResult) => {
      const { errors } = result.data.changePeriodGroupPrivileges
      if (!errors.length) {
        periodGroupPrivilegesUpdate(cache, result)
      }
    }
    const changeUsersPrivilegesUpdate = (cache: DataProxy, result: ChangeGroupUsersPrivilegesMutationResult) => {
      const { success } = result.data.changeGroupUsersPrivileges
      if (success) {
        props.update(cache, result)
      }
    }
    return {
      headers,
      itemName,
      privileges,
      loading,
      selectPrivileges,
      formVariables,
      mutationName,
      changePeriodGroupPrivileges,
      changeGroupUsersPrivileges,
      changeGroupPrivilegesUpdate,
      changeUsersPrivilegesUpdate
    }
  }
})
</script>
