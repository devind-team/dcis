<template lang="pug">
  v-menu(v-model="active" bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-list
      mutation-modal-form(
        :header="String($t('dcis.periods.changePeriodUsers.header'))"
        :button-text="String($t('dcis.periods.changePeriodUsers.buttonText'))"
        :mutation="changePeriodGroupUsers"
        :variables="{ periodGroupId: periodGroup.id, usersIds: selectUsers }"
        :update="changePeriodGroupUsersUpdate"
        mutation-name="changePeriodGroupUsers"
        errors-in-alert
        persistent
        @close="close"
      )
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-account-multiple-plus
            v-list-item-title Добавить
        template(#form)
          v-autocomplete(
            v-model="selectUsers"
            :label="$t('ac.users.components.changeUsers.users')"
            :items="allUsers"
            :search-input.sync="search"
            :loading="loading"
            item-text="text"
            item-value="id"
            chips
            deletable-chips
            multiple
            clearable
            hide-selected
            hide-no-data
            @change="search=''"
          )
      v-list-item
        v-list-item-icon
          v-icon mdi-account-switch
        v-list-item-title Скопировать из сбора
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { computed, defineComponent, inject, PropType, ref } from '#app'
import {
  ChangePeriodGroupUsersMutationPayload,
  PeriodGroupType,
  UsersQuery,
  UsersQueryVariables,
  UserType
} from '~/types/graphql'
import changePeriodGroupUsers from '~/gql/dcis/mutations/project/change_period_group_users.graphql'
import { useDebounceSearch, useFilters, useQueryRelay } from '~/composables'
import usersQuery from '~/gql/core/queries/users.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type GroupUser = {
  id: string | number
  value: UserType
  text: string
}

export type ChangePeriodGroupUsersMutationResult = { data: { changePeriodGroupUsers: ChangePeriodGroupUsersMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    periodGroup: { type: Object as PropType<PeriodGroupType>, required: true }
  },
  setup (props) {
    const { search, debounceSearch } = useDebounceSearch()
    const { dateTimeHM, getUserFullName } = useFilters()
    const active = ref<boolean>(false)
    const selectUsers = ref<UserType[] | null>(null)
    const {
      loading,
      data: users
    } = useQueryRelay<UsersQuery, UsersQueryVariables, UserType>({
      document: usersQuery,
      variables: () => ({
        search: debounceSearch.value
      }),
      options: { enabled: active }
    })
    const filterUsers = computed<UserType[]>(() => {
      return users
        ? users.value.filter(user => !props.periodGroup.users.find(groupUser => user.id === groupUser.id))
        : []
    })
    const allUsers = computed<GroupUser[]>(() => {
      return filterUsers.value.map(user => ({
        id: user.id,
        value: user,
        text: getUserFullName(user)
      }))
    })
    const periodGroupUsersUpdate: any = inject('periodGroupUsersUpdate')
    const changePeriodGroupUsersUpdate = (cache: DataProxy, result: ChangePeriodGroupUsersMutationResult) => {
      const { success } = result.data.changePeriodGroupUsers
      if (success) {
        periodGroupUsersUpdate(cache, result)
      }
    }
    const close = (): void => {
      selectUsers.value = null
    }
    return {
      active,
      users,
      loading,
      changePeriodGroupUsers,
      selectUsers,
      allUsers,
      search,
      dateTimeHM,
      close,
      changePeriodGroupUsersUpdate
    }
  }
})
</script>
