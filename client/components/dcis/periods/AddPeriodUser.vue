<template lang="pug">
mutation-modal-form(
  ref="form"
  :header="String($t('dcis.periods.users.addUser.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.users.addUser.buttonText'))"
  :mutation="addPeriodUserMutation"
  :variables="variables"
  :update="update"
  :mutation-name="['changeUserPeriodGroups', 'changeUserPeriodPrivileges']"
  errors-in-alert
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.users.addUser.user'))"
      rules="required"
    )
      v-autocomplete(
        v-model="userId"
        :label="$t('dcis.periods.users.addUser.user')"
        :items="users"
        :loading="usersLoading"
        :search-input.sync="usersSearch"
        :error-messages="errors"
        :success="valid"
        item-value="id"
        no-filter
      )
        template(#selection="{ item }") {{ getUserFullName(item) }}
        template(#item="{ item }")
          v-list-item-avatar
            avatar-menu(:user="item")
          v-list-item-content
            v-list-item-title {{ getUserFullName(item) }}
          v-list-item-action(v-if="periodUsers.find((user) => user.id === item.id)")
            v-tooltip(bottom)
              template(#activator="{ on }")
                v-icon(v-on="on" color="red") mdi-alert
              span {{ $t('dcis.periods.users.addUser.userExistWarning') }}
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.users.addUser.groups'))"
      vid="groups"
      :rules="{ required_if: { target: 'privileges', values: [''] } }"
    )
      v-autocomplete(
        v-model="periodGroupIds"
        :label="$t('dcis.periods.users.addUser.groups')"
        :items="period.periodGroups"
        :error-messages="errors"
        :success="valid"
        item-value="id"
        item-text="name"
        chips
        deletable-chips
        multiple
        hide-selected
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.users.addUser.privileges'))"
      vid="privileges"
      :rules="{ required_if: { target: 'groups', values: [''] } }"
    )
     v-autocomplete(
       v-model="privilegeIds"
       :label="$t('dcis.periods.users.addUser.privileges')"
       :items="privileges"
       :loading="privilegesLoading"
       :error-messages="errors"
       :success="valid"
       item-value="id"
       item-text="name"
       chips
       deletable-chips
       multiple
       hide-selected
     )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { VariablesParameter } from '@vue/apollo-composable/dist/useQuery'
import { PropType } from '#app'
import {
  UserType,
  PeriodType,
  PrivilegesQuery,
  PrivilegesQueryVariables,
  UsersQuery,
  UsersQueryVariables,
  AddPeriodUserMutationVariables,
  ChangeUserPeriodGroupsMutationPayload,
  ChangeUserPeriodPrivilegesPayload
} from '~/types/graphql'
import usersQuery from '~/gql/core/queries/users.graphql'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import addPeriodUserMutation from '~/gql/dcis/mutations/period/add_period_user.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

export type AddPeriodUserMutationResult = {
  data: {
    changeUserPeriodGroups: ChangeUserPeriodGroupsMutationPayload
    changeUserPeriodPrivileges: ChangeUserPeriodPrivilegesPayload
  }
}
type UpdateFunction = (cache: DataProxy, result: AddPeriodUserMutationResult) => DataProxy

export default defineComponent({
  components: { MutationModalForm, AvatarDialog },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    periodUsers: { type: Array as PropType<PeriodType[]>, default: () => [] },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const form = ref<InstanceType<typeof MutationModalForm> | null>(null)
    onMounted(() => {
      watch(() => form.value.active, (value: boolean) => {
        if (value) {
          options.value.enabled = true
        }
      })
    })

    const { getUserFullName } = useFilters()

    const userId = ref<string | null>(null)
    const periodGroupIds = ref<string[]>([])
    const privilegeIds = ref<string[]>([])

    const options = ref<{ enabled: boolean }>({ enabled: false })

    const { search: usersSearch, debounceSearch: usersDebounceSearch } = useDebounceSearch()
    const {
      data: users,
      loading: usersLoading
    } = useQueryRelay<UsersQuery, UsersQueryVariables, UserType>({
      document: usersQuery,
      options,
      variables: () => {
        const result: VariablesParameter<UsersQueryVariables> = { search: usersDebounceSearch.value }
        if (usersDebounceSearch.value) {
          result.first = undefined
        }
        return result
      }
    })

    const { data: privileges, loading: privilegesLoading } = useCommonQuery<
      PrivilegesQuery,
      PrivilegesQueryVariables
    >({
      document: privilegesQuery,
      options
    })

    const variables = computed<AddPeriodUserMutationVariables>(() => ({
      userId: userId.value,
      periodId: props.period.id,
      periodGroupIds: periodGroupIds.value,
      privilegesIds: privilegeIds.value
    }))

    const close = () => {
      userId.value = null
      periodGroupIds.value = []
      privilegeIds.value = []
    }

    return {
      form,
      addPeriodUserMutation,
      getUserFullName,
      userId,
      periodGroupIds,
      privilegeIds,
      usersSearch,
      users,
      usersLoading,
      privileges,
      privilegesLoading,
      variables,
      close
    }
  }
})
</script>
