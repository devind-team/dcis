<template lang="pug">
  v-card(v-if="periodGroup" flat)
    v-navigation-drawer(
      v-model="active"
      width="40vw"
      app
      right
      bottom
      temporary
    )
      v-card.ma-2.transparent(v-if="selectUser" flat)
        v-card-subtitle.text-h6.text-center {{ $t('dcis.periods.changePrivileges.privileges') }} {{ getUserFullName(selectUser) }}
        v-divider
        v-card-text(v-if="userPrivileges")
          v-data-table.transparent(
            :headers="additionalHeaders"
            :loading="loading"
            :items="userPrivileges"
            hide-default-footer
            disable-pagination
          )
          v-divider
          v-card-actions.d-flex.flex-wrap.justify-center
            period-group-privileges(
              :period-group="periodGroup"
              :period="period"
              :user="selectUser"
              :user-privileges="userPrivileges"
              :update="changeGroupUsersPrivilegesUpdate"
              :active-query="active"
            )
              template(#activator="{ on }")
                v-btn(v-on="on" color="primary") {{ $t('dcis.periods.changePrivileges.add') }}
            v-spacer
            delete-menu(
              :itemName="getUserFullName(selectUser)"
              @confirm="deleteUserFromPeriodGroupMutate({ userId: selectUser.id, periodGroupId: Number(periodGroup.id) }).then()"
            )
              template(#default="{ on }")
                v-btn(v-on="on" color="error") {{ $t('dcis.periods.changePrivileges.deleteUser') }}
    v-card-actions
      period-group-privileges(:period-group="periodGroup" :key="periodGroup.id" active-query)
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ $t('dcis.periods.changePrivileges.change') }}
      v-spacer
      add-period-group-users(:period-group="periodGroup" active-query)
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ $t('dcis.periods.changePeriodUsers.addUsers') }}
    v-card-text
      v-data-table(
        :headers="headers"
        :items="periodGroup.users"
        disable-pagination
        hide-default-footer
      )
        template(#item.avatar="{ item }")
          avatar-dialog(:item="item")
        template(#item.name="{ item }")
          a(@click="selectedUser(item.id)") {{ getUserFullName(item) }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify'
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import { computed, defineComponent, PropType, ref } from '#app'
import {
  PeriodGroupType,
  PeriodType,
  UserGroupPrivilegesQuery,
  UserGroupPrivilegesQueryVariables,
  UserType,
  DeleteUserFromPeriodGroupMutation,
  DeleteUserFromPeriodGroupMutationVariables,
  DeleteUserFromPeriodGroupMutationPayload
} from '~/types/graphql'
import { useCommonQuery, useFilters, useI18n } from '~/composables'
import userGroupPrivilegesQuery from '~/gql/dcis/queries/user_group_privileges.graphql'
import deleteUserFromPeriodGroup from '~/gql/dcis/mutations/project/delete_user_from_period_group.graphql'
import changeGroupUsersPrivileges from '~/gql/dcis/mutations/privelege/change_user_privileges.graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import AddPeriodGroupUsers from '~/components/dcis/periods/AddPeriodGroupUsers.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import PeriodGroupPrivileges, {
  ChangeGroupUsersPrivilegesMutationResult
} from '~/components/dcis/periods/PeriodGroupPrivileges.vue'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type DeleteUserFromPeriodGroupMutationResult = { data: { deleteUserFromPeriodGroup: DeleteUserFromPeriodGroupMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: DeleteUserFromPeriodGroupMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { AvatarDialog, AddPeriodGroupUsers, PeriodGroupPrivileges, MutationModalForm, DeleteMenu },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    periodGroup: { type: Object as PropType<PeriodGroupType>, default: null },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { getUserFullName } = useFilters()
    const { t } = useI18n()

    const selectUser = ref<UserType | null>(null)
    const active = computed<boolean>({
      get: () => (!!selectUser.value),
      set: (value: boolean): void => {
        if (!value) {
          selectUser.value = null
        }
      }
    })
    const options = ref({ enabled: active, fetchPolicy: 'cache-and-network' as const })
    const { data: userPrivileges, loading, update } = useCommonQuery<UserGroupPrivilegesQuery, UserGroupPrivilegesQueryVariables>({
      document: userGroupPrivilegesQuery,
      variables: () => ({ userId: selectUser.value?.id, periodGroupId: props.periodGroup.id }),
      options: options.value
    })

    const additionalHeaders = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.changePrivileges.name') as string, value: 'name' },
      { text: t('dcis.periods.changePrivileges.key') as string, value: 'key' }
    ]))
    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.changePeriodUsers.avatar') as string, value: 'avatar' },
      { text: t('dcis.periods.changePeriodUsers.name') as string, value: 'name' },
      { text: t('dcis.periods.changePeriodUsers.jobPost') as string, value: '' },
      { text: t('dcis.periods.changePeriodUsers.division') as string, value: '' }
    ]))

    /**
     * Обновление после изменения привилегий пользователя
     * @param cache
     * @param result
     */
    const changeGroupUsersPrivilegesUpdate = (cache: DataProxy, result: ChangeGroupUsersPrivilegesMutationResult) => {
      const { errors } = result.data.changeGroupUsersPrivileges
      if (!errors.length) {
        update(
          cache,
          result,
          (dataCache, { data: { changeGroupUsersPrivileges: { privileges } } }: ChangeGroupUsersPrivilegesMutationResult) => {
            dataCache.userPrivileges = privileges
            return dataCache
          })
      }
    }
    const selectedUser = (userId: string): void => {
      selectUser.value = props.periodGroup.users.find(user => user.id === userId)
    }

    /**
     * Обновление после удаления пользователя из группы
     * @param cache
     * @param result
     */
    const deleteUserUpdate = (cache, result) => {
      const { errors } = result.data.deleteUserFromPeriodGroup
      if (!errors.length) {
        props.update(cache, result)
        update(cache, result, (dataCache) => {
          dataCache.userPrivileges = []
          return dataCache
        })
        selectUser.value = null
        active.value = false
      }
    }
    const { mutate: deleteUserFromPeriodGroupMutate } =
     useMutation<DeleteUserFromPeriodGroupMutation, DeleteUserFromPeriodGroupMutationVariables>(deleteUserFromPeriodGroup, {
       update: deleteUserUpdate
     })
    return {
      active,
      headers,
      additionalHeaders,
      getUserFullName,
      selectUser,
      loading,
      userPrivileges,
      selectedUser,
      changeGroupUsersPrivileges,
      changeGroupUsersPrivilegesUpdate,
      deleteUserFromPeriodGroupMutate
    }
  }
})
</script>
