<template lang="pug">
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
      slot(name="activator" :on="on")
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
        hide-no-data
        @change="search=''"
      )
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
    periodGroup: { type: Object as PropType<PeriodGroupType>, required: true },
    activeQuery: { type: Boolean, default: false }
  },
  setup (props) {
    const { search, debounceSearch } = useDebounceSearch()
    const { dateTimeHM, getUserFullName } = useFilters()

    const selectUsers = ref<UserType[] | null>(null)
    const options = ref({ enabled: props.activeQuery })
    const {
      loading,
      data: users
    } = useQueryRelay<UsersQuery, UsersQueryVariables, UserType>({
      document: usersQuery,
      variables: () => ({
        search: debounceSearch.value
      }),
      options: options.value
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

    // Обновление после добавления пользователей в группу
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
