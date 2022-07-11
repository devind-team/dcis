<template lang="pug">
mutation-modal-form(
  :header="formHeader"
  :subheader="itemName"
  :button-text="buttonText"
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
      :items="items"
      :loading="loading"
      item-key="id"
      disable-pagination
      show-select
      hide-default-footer
    )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader } from 'vuetify'
import { computed, defineComponent, inject, PropType, ref } from '#app'
import {
  AdditionalPrivilegesQuery,
  AdditionalPrivilegesQueryVariables,
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
import { useCommonQuery, useFilters, useI18n } from '~/composables'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import additionalPrivilegesQuery from '~/gql/dcis/queries/additional_privileges.graphql'
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
    const { data: privileges, loading } = useCommonQuery<PrivilegesQuery, PrivilegesQueryVariables>({
      document: privilegesQuery
    })
    const { data: additionalPrivileges } = useCommonQuery<AdditionalPrivilegesQuery, AdditionalPrivilegesQueryVariables>({
      document: additionalPrivilegesQuery,
      variables: { periodId: props.period?.id, userId: props.user?.id },
      options: props.user ? options.value : { enabled: false }
    })
    const privilegesListId = ref<string[]>([])
    const selectPrivileges = computed<PrivilegeType[]>({
      get: (): PrivilegeType[] => props.user ? additionalPrivileges.value?.map((e: PrivilegeType) => e) : props.periodGroup.privileges,
      set: (value: PrivilegeType[]) => {
        privilegesListId.value = value.map((e: PrivilegeType) => e.id)
      }
    })
    const items = computed<PrivilegeType[]>(() => props.user
      ? privileges.value.filter((privilege: PrivilegeType) => !props.periodGroup.privileges.map((p: PrivilegeType) => p.id).includes(privilege.id))
      : privileges.value.map((privilege: PrivilegeType) => privilege)
    )
    const itemName = computed<string>(() => (props.user ? getUserFullName(props.user) : props.periodGroup.name))
    const mutationName = computed<string>(() => (props.user ? 'changeGroupUsersPrivileges' : 'changePeriodGroupPrivileges'))
    const formVariables = computed<{ periodGroupId: string, privilegesIds: string[], userId?: string }>(() => {
      if (props.user) {
        return { periodGroupId: props.periodGroup.id, userId: props.user.id, privilegesIds: privilegesListId.value }
      } else {
        return { periodGroupId: props.periodGroup.id, privilegesIds: privilegesListId.value }
      }
    })
    const formHeader = computed<string>(() => (props.user
      ? t('dcis.periods.changePrivileges.userHeader') as string
      : t('dcis.periods.changePrivileges.groupHeader') as string)
    )
    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.changePrivileges.name') as string, value: 'name' },
      { text: t('dcis.periods.changePrivileges.key') as string, value: 'key' }
    ]))
    const buttonText = computed<string>(() => (props.user
      ? t('dcis.periods.changePrivileges.buttonAddText') as string
      : t('dcis.periods.changePrivileges.buttonChangeText') as string)
    )
    const periodGroupPrivilegesUpdate: any = inject('periodGroupPrivilegesUpdate')

    /**
     * Обновление после изменения привилегий группы
     * @param cache
     * @param result
     */
    const changeGroupPrivilegesUpdate = (cache: DataProxy, result: ChangePeriodGroupPrivilegesMutationResult) => {
      const { errors } = result.data.changePeriodGroupPrivileges
      if (!errors.length) {
        periodGroupPrivilegesUpdate(cache, result)
      }
    }

    /**
     * Обновление после изменения привилегий пользователя
     * @param cache
     * @param result
     */
    const changeUsersPrivilegesUpdate = (cache: DataProxy, result: ChangeGroupUsersPrivilegesMutationResult) => {
      const { success } = result.data.changeGroupUsersPrivileges
      if (success) {
        props.update(cache, result)
      }
    }
    return {
      headers,
      items,
      itemName,
      formHeader,
      privileges,
      buttonText,
      additionalPrivileges,
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
