<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.copyPeriodGroups.header'))"
    :button-text="String($t('dcis.periods.copyPeriodGroups.buttonText'))"
    :mutation="copyPeriodGroups"
    :variables="{ periodId: selectPeriod.id }"
    :update="copyPeriodGroupsUpdate"
    mutation-name="copyPeriodGroups"
    errors-in-alert
    persistent
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-autocomplete(
        v-model="selectPeriod"
        :label="$t('ac.users.components.changeUsers.users')"
        :items="periods"
        :search-input.sync="search"
        :loading="loading"
        item-text="name"
        item-value="id"
        clearable
        hide-no-data
      )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { ChangePeriodGroupUsersMutationResult } from './AddPeriodGroupUsers.vue'
import { defineComponent, inject } from '#app'
import changePeriodGroupUsers from '~/gql/dcis/mutations/project/change_period_group_users.graphql'
import { useDebounceSearch } from '~/composables'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { PeriodType } from '~/types/graphql'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    activeQuery: { type: Boolean, default: false }
  },
  setup (props) {
    const { search, debounceSearch } = useDebounceSearch()

    const selectPeriod = ref<PeriodType | null>(null)

    const options = ref({ enabled: props.activeQuery })
    const { data: periods, loading } = useCommonQuery<UserPrivilegesQuery, UserPrivilegesQueryVariables>({
      document: periodsQuery,
      variables: () => ({
        search: debounceSearch.value
      }),
      options: options.value
    })

    // Обновление после добавления пользователей в группу
    const periodGroupUsersUpdate: any = inject('periodGroupUsersUpdate')
    const copyPeriodGroupsUpdate = (cache: DataProxy, result: ChangePeriodGroupUsersMutationResult) => {
      const { success } = result.data.changePeriodGroupUsers
      if (success) {
        periodGroupUsersUpdate(cache, result)
      }
    }
    return {
      changePeriodGroupUsers,
      selectPeriod,
      search,
      close,
      copyPeriodGroupsUpdate
    }
  }
})
</script>
