<template lang="pug">
mutation-modal-form(
  ref="form"
  :header="String($t('curators.changeCuratorGroupUsers.header'))"
  :subheader="curatorGroup.name"
  :button-text="String($t('curators.changeCuratorGroupUsers.buttonText'))"
  :mutation="addUsersCuratorGroupMutation"
  :variables="addVariables"
  :update="addUsersUpdate"
  :success-close="false"
  :success-message="String($t('curators.changeCuratorGroupUsers.successMessage'))"
  mutation-name="addUsersCuratorGroup"
  i18n-path="curators.changeCuratorGroupUsers"
  width="1000"
  @close="close"
  @done="addUsersDone"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    v-data-table(
      :headers="headers"
      :items="groupUsers"
      :loading="curatorGroupLoading"
      disable-pagination
      hide-default-footer
    )
      template(#item.avatar="{ item }")
        avatar-dialog(:item="item")
      template(#item.name="{ item }") {{ getUserFullName(item) }}
      template(#item.actions="{ item }")
        delete-menu(
          :item-name="String($t('curators.changeCuratorGroupUsers.deleteItemName'))"
          @confirm="deleteUser({ curatorGroupId: curatorGroup.id, userId: item.id })"
        )
          template(#default="{ on: onMenu }")
            v-tooltip(bottom)
              template(#activator="{ on: onTooltip, attrs }")
                v-btn.ml-1(v-on="{ ...onMenu, ...onTooltip }" v-bind="attrs" color="error" icon)
                  v-icon mdi-delete
              span {{ $t('curators.changeCuratorGroupUsers.deleteTooltip') }}
    validation-provider(
      ref="newUsersValidationProvider"
      v-slot="{ errors, valid }"
      :name="String($t('curators.changeCuratorGroupUsers.newUsers'))"
      rules="required"
    )
      v-autocomplete.mt-2(
        v-model="newUsers"
        :label="$t('curators.changeCuratorGroupUsers.newUsers')"
        :items="users"
        :loading="usersLoading"
        :search-input.sync="usersSearch"
        :error-messages="errors"
        :success="valid"
        item-value="id"
        multiple
        chips
        deletable-chips
        return-object
        no-filter
      )
        template(#selection="{ item }")
          v-chip(close @click:close="userChipClose(item)") {{ getUserFullName(item) }}
        template(#item="{ item }")
          v-list-item-avatar
            avatar-dialog(:item="item")
          v-list-item-content
            v-list-item-title {{ getUserFullName(item) }}
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, PropType, ref } from '#app'
import { DataProxy } from '@apollo/client'
import { VariablesParameter } from '@vue/apollo-composable/dist/useQuery'
import { useMutation } from '@vue/apollo-composable'
import { watchOnce } from '@vueuse/core'
import { DataTableHeader } from 'vuetify'
import { ValidationProvider } from 'vee-validate'
import {
  UserType,
  UserFieldsFragment,
  CuratorGroupType,
  CuratorGroupUsersQuery,
  CuratorGroupUsersQueryVariables,
  CuratorGroupNewUsersQuery,
  CuratorGroupNewUsersQueryVariables,
  DeleteUserCuratorGroupMutation,
  DeleteUserCuratorGroupMutationVariables,
  AddUsersCuratorGroupMutationVariables,
  AddUsersCuratorGroupPayload
} from '~/types/graphql'
import { useCommonQuery, useQueryRelay, useI18n, useFilters } from '~/composables'
import curatorGroupUsersQuery from '~/gql/dcis/queries/curator_group_users.graphql'
import curatorGroupNewUsersQuery from '~/gql/dcis/queries/curator_group_new_users.graphql'
import addUsersCuratorGroupMutation from '~/gql/dcis/mutations/curator/add_users_curator_group.graphql'
import deleteUserCuratorGroupMutation from '~/gql/dcis/mutations/curator/delete_user_curator_group.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type AddUsersCuratorGroupResult = { data: { addUsersCuratorGroup: AddUsersCuratorGroupPayload } }

export default defineComponent({
  components: { MutationModalForm, AvatarDialog, DeleteMenu },
  props: {
    curatorGroup: { type: Object as PropType<CuratorGroupType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()
    const { getUserFullName } = useFilters()

    const form = ref<InstanceType<typeof MutationModalForm> | null>(null)
    const newUsersValidationProvider = ref<InstanceType<typeof ValidationProvider | null>>(null)
    onMounted(() => {
      watchOnce(() => form.value.active, (value: boolean) => {
        options.value.enabled = value
      })
    })

    const headers = computed<DataTableHeader[]>(() => [
      {
        text: t('curators.changeCuratorGroupUsers.tableHeaders.avatar') as string,
        value: 'avatar',
        align: 'center',
        sortable: false
      },
      { text: t('curators.changeCuratorGroupUsers.tableHeaders.name') as string, value: 'name' },
      { text: t('curators.changeCuratorGroupUsers.tableHeaders.username') as string, value: 'username' },
      { text: t('curators.changeCuratorGroupUsers.tableHeaders.email') as string, value: 'email' },
      {
        text: t('curators.changeCuratorGroupUsers.tableHeaders.actions') as string,
        value: 'actions',
        align: 'center',
        sortable: false
      }
    ])

    const options = ref<{ enabled: boolean }>({ enabled: false })

    const { data: curatorGroup, loading: curatorGroupLoading, update: curatorGroupUpdate } = useCommonQuery<
      CuratorGroupUsersQuery,
      CuratorGroupUsersQueryVariables
    >({
      document: curatorGroupUsersQuery,
      options,
      variables: () => ({ curatorGroupId: props.curatorGroup.id })
    })
    const groupUsers = computed<UserFieldsFragment[]>(() => curatorGroup.value ? curatorGroup.value.users : [])

    const { mutate: deleteUserMutate } = useMutation<
      DeleteUserCuratorGroupMutation,
      DeleteUserCuratorGroupMutationVariables
    >(deleteUserCuratorGroupMutation, {
      update: (cache, result) => curatorGroupUpdate(
        cache,
        result,
        (
          dataCache,
          { data: { deleteUserCuratorGroup: { success, id } } }
        ) => {
          if (success) {
            dataCache.curatorGroup.users = dataCache.curatorGroup.users.filter(
              (user: UserFieldsFragment) => user.id !== id
            )
          }
          return dataCache
        }
      )
    })
    const deleteUser = async (variables: DeleteUserCuratorGroupMutationVariables) => {
      await deleteUserMutate(variables)
      await refetchUsers()
    }

    const { search: usersSearch, debounceSearch: usersDebounceSearch } = useDebounceSearch()
    const {
      data: users,
      loading: usersLoading,
      refetch: refetchUsers
    } = useQueryRelay<CuratorGroupNewUsersQuery, CuratorGroupNewUsersQueryVariables, UserType>({
      document: curatorGroupNewUsersQuery,
      options,
      variables: () => {
        const result: VariablesParameter<CuratorGroupNewUsersQueryVariables> = {
          search: usersDebounceSearch.value,
          curatorGroupId: props.curatorGroup.id
        }
        if (usersDebounceSearch.value) {
          result.first = undefined
        }
        return result
      }
    })
    const newUsers = ref<UserType[]>([])
    const userChipClose = (user: UserType) => {
      newUsers.value = newUsers.value.filter((existUser: UserType) => existUser.id !== user.id)
    }
    const addVariables = computed<AddUsersCuratorGroupMutationVariables>(() => ({
      curatorGroupId: props.curatorGroup.id,
      userIds: newUsers.value.map((user: UserType) => user.id)
    }))
    const addUsersUpdate = (cache: DataProxy, result: AddUsersCuratorGroupResult) => {
      curatorGroupUpdate(
        cache,
        result,
        (dataCache, { data: { addUsersCuratorGroup: { success, users } } }) => {
          if (success) {
            dataCache.curatorGroup.users = [...dataCache.curatorGroup.users, ...(users as UserFieldsFragment[])]
            dataCache.curatorGroup.users.sort((u1: UserFieldsFragment, u2: UserFieldsFragment) => {
              return Number(new Date(u2.createdAt)) - Number(new Date(u1.createdAt))
            })
          }
          return dataCache
        }
      )
    }
    const addUsersDone = () => {
      newUsers.value = []
      newUsersValidationProvider.value.reset()
      refetchUsers()
    }

    const close = () => {
      newUsers.value = []
    }

    return {
      addUsersCuratorGroupMutation,
      getUserFullName,
      form,
      newUsersValidationProvider,
      headers,
      groupUsers,
      deleteUser,
      curatorGroupLoading,
      usersSearch,
      users,
      usersLoading,
      refetchUsers,
      newUsers,
      userChipClose,
      addVariables,
      addUsersUpdate,
      addUsersDone,
      close
    }
  }
})
</script>
