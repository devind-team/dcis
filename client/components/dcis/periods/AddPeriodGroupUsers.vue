<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.changePeriodUsers.header'))"
    :button-text="String($t('dcis.periods.changePeriodUsers.buttonText'))"
    :mutation="changePeriodGroupUsers"
    :variables="formVariables"
    :update="changePeriodGroupUsersUpdate"
    mutation-name="changePeriodGroupUsers"
    errors-in-alert
    persistent
    @close="close"
    @done="selectUsers = []"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="$t('dcis.periods.changePeriodUsers.users')"
        rules="required"
      )
        v-combobox(
          v-model="selectUsers"
          :search-input.sync="search"
          :loading="loading"
          :items="allUsers"
          :label="$t('dcis.periods.changePeriodUsers.users')"
          :filter="filterInputUsers"
          :success="valid"
          :error-messages="errors"
          multiple
          return-object
          item-text="text"
          item-value="value"
          hide-selected
          clearable
        )
          template(#selection="{ item }")
            v-chip.ma-1(
              v-model="item"
              :key="item.id"
              close
              @click:close="selectUsers.splice(selectUsers.indexOf(item), 1)"
            ) {{ item.text }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { computed, defineComponent, inject, PropType, ref } from '#app'
import {
  ChangePeriodGroupUsersMutationPayload,
  PeriodGroupType,
  ChangePeriodGroupUsersMutationVariables,
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

    const selectUsers = ref<GroupUser[] | null>([])
    const formVariables = computed<ChangePeriodGroupUsersMutationVariables>(() => ({
      periodGroupId: props.periodGroup.id,
      usersIds: selectUsers.value.map((user: GroupUser) => (user.id || null))
    }))
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
    const filterInputUsers = (item: GroupUser, queryText: string): boolean => {
      const qt: string = queryText.toLowerCase()
      return item.text.toLowerCase().split(' ').some((word: string) => word.includes(qt))
    }

    const periodGroupUsersUpdate: any = inject('periodGroupUsersUpdate')
    const changePeriodGroupUsersUpdate = (cache: DataProxy, result: ChangePeriodGroupUsersMutationResult) => {
      const { success } = result.data.changePeriodGroupUsers
      if (success) {
        periodGroupUsersUpdate(cache, result)
      }
    }
    const close = (): void => {
      selectUsers.value = []
    }
    return {
      users,
      loading,
      changePeriodGroupUsers,
      selectUsers,
      filterInputUsers,
      formVariables,
      allUsers,
      search,
      dateTimeHM,
      close,
      changePeriodGroupUsersUpdate
    }
  }
})
</script>
