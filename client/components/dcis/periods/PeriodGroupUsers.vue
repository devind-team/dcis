<template lang="pug">
  v-card(v-if="periodGroup" flat)
    v-navigation-drawer(
      v-model="active"
      width="35vw"
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
            )
              template(#activator="{ on }")
                v-btn(v-on="on" color="primary") {{ $t('dcis.periods.changePrivileges.change') }}
    v-card-actions
      add-period-group-users(v-slot="{ on }" :period-group="periodGroup")
        v-btn(v-on="on" color="primary") {{ $t('dcis.periods.changePeriodUsers.addUsers') }}
      v-spacer
      period-group-privileges(:period-group="periodGroup" :key="periodGroup.id" active-query)
        template(#activator="{ on }")
          v-btn(v-on="on" color="primary") {{ $t('dcis.periods.changePrivileges.change') }}
    v-card-text
      v-data-table(
        :headers="headers"
        :items="periodGroup.users"
        hide-default-footer
      )
        template(#item.avatar="{ item }")
          avatar-dialog(:item="item")
        template(#item.name="{ item }")
          a(@click="selectedUser(item.id)") {{ getUserFullName(item) }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import { DataProxy } from 'apollo-cache'
import { PeriodGroupType, PeriodType, UserPrivilegesQuery, UserPrivilegesQueryVariables, UserType } from '~/types/graphql'
import { useCommonQuery, useFilters, useI18n } from '~/composables'
import userPrivilegesQuery from '~/gql/dcis/queries/user_privileges.graphql'
import changeGroupUsersPrivileges from '~/gql/dcis/mutations/privelege/change_user_privileges.graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import AddPeriodGroupUsers from '~/components/dcis/periods/AddPeriodGroupUsers.vue'
import PeriodGroupPrivileges, {
  ChangeGroupUsersPrivilegesMutationResult
} from '~/components/dcis/periods/PeriodGroupPrivileges.vue'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { AvatarDialog, AddPeriodGroupUsers, PeriodGroupPrivileges, MutationModalForm },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    periodGroup: { type: Object as PropType<PeriodGroupType>, default: null }
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
    const options = ref({ enabled: active })
    const { data: userPrivileges, loading, update } = useCommonQuery<UserPrivilegesQuery, UserPrivilegesQueryVariables>({
      document: userPrivilegesQuery,
      variables: () => ({ userId: selectUser.value?.id, periodId: props.period.id }),
      options: options.value
    })
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
      changeGroupUsersPrivilegesUpdate
    }
  }
})
</script>
