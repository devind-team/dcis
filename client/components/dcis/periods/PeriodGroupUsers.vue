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
        v-card-subtitle.text-h6.text-center Привилегии пользователя {{ getUserFullName(selectUser) }}
        v-divider
        v-card-text
          v-data-table.transparent(
            :headers="additionalHeaders"
            :loading="loading"
            :items="periodPrivileges"
            hide-default-footer
            disable-pagination
          )
          v-divider
          v-card-actions.d-flex.flex-wrap.justify-center(v-if="selectPrivileges")
            mutation-modal-form(
              :header="String($t('dcis.periods.changeGroupUsersPrivileges.header'))"
              :button-text="String($t('dcis.periods.changeGroupUsersPrivileges.buttonText'))"
              :mutation="changeGroupUsersPrivileges"
              :variables="{ periodId: period.id, userId: selectUser.id, privilegesIds: selectPrivileges.map(e => e.id) }"
              :update="changeGroupUsersPrivilegesUpdate"
              mutation-name="changeGroupUsersPrivileges"
              errors-in-alert
              persistent
            )
              template(#activator="{ on }")
                v-btn(v-on="on" color="primary") Изменить привилегии
              template(#form)
                v-data-table(
                  v-model="selectPrivileges"
                  :headers="additionalHeaders"
                  :items="periodGroup.privileges"
                  item-key="id"
                  show-select
                  hide-default-footer
                )
    v-card-actions
      add-period-group-users(
        v-slot="{ on }"
        :period-group="periodGroup"
      )
        v-btn(v-on="on" color="primary") Добавить пользователей
      v-spacer
      period-group-privileges(
        v-slot="{ on }"
        :period-group="periodGroup"
        :key="periodGroup.id"
      )
        v-btn(v-on="on" class="align-self-center" icon text)
          v-icon mdi-cog
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
import {
  AddPeriodMutationPayload,
  ChangeGroupUserPrivilegesMutationPayload,
  PeriodGroupType,
  PeriodPrivilegesQuery,
  PeriodPrivilegesQueryVariables,
  PeriodType,
  PrivilegeType,
  UserType
} from '~/types/graphql'
import { useCommonQuery, useFilters, useI18n } from '~/composables'
import periodPrivilegesQuery from '~/gql/dcis/queries/period_privileges.graphql'
import changeGroupUsersPrivileges from '~/gql/dcis/mutations/privelege/change_user_privileges.graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import AddPeriodGroupUsers from '~/components/dcis/periods/AddPeriodGroupUsers.vue'
import PeriodGroupPrivileges from '~/components/dcis/periods/PeriodGroupPrivileges.vue'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type ChangeGroupUsersPrivilegesMutationResult = { data: { changeGroupUsersPrivileges: ChangeGroupUserPrivilegesMutationPayload } }

export default defineComponent({
  components: { AvatarDialog, AddPeriodGroupUsers, PeriodGroupPrivileges, MutationModalForm },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    periodGroup: { type: Object as PropType<PeriodGroupType>, default: null }
  },
  setup (props) {
    const { dateTimeHM, getUserFullName } = useFilters()
    const { t } = useI18n()
    const selectUser = ref<UserType | null>(null)
    const selectPrivileges = ref<any>(null)
    const active = computed<boolean>({
      get: () => (!!selectUser.value),
      set: (value: boolean): void => {
        if (!value) {
          selectUser.value = null
        }
      }
    })
    const options = ref({ enabled: active })
    const { data: periodPrivileges, loading, variables, changeUpdate } = useCommonQuery<PeriodPrivilegesQuery, PeriodPrivilegesQueryVariables>({
      document: periodPrivilegesQuery,
      variables: { userId: selectUser.value?.id, periodId: props.period.id },
      options: options.value
    })
    const changeGroupUsersPrivilegesUpdate = (cache: DataProxy, result: ChangeGroupUsersPrivilegesMutationResult) => {
      const { success } = result.data.changeGroupUsersPrivileges
      if (success) {
        changeUpdate(cache, result, 'privileges')
      }
    }
    const selectedUser = (userId: string): void => {
      variables.value = { userId, periodId: props.period.id }
      selectUser.value = props.periodGroup.users.find(user => user.id === userId)
    }
    watchEffect(() => {
      selectPrivileges.value = periodPrivileges.value
    })
    const additionalHeaders = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.privileges.name') as string, value: 'name' },
      { text: t('dcis.periods.privileges.key') as string, value: 'key' }
    ]))
    const headers: DataTableHeader[] = [
      { text: 'Аватар', value: 'avatar' },
      { text: 'ФИО', value: 'name' },
      { text: 'Должность', value: '' },
      { text: 'Департамент', value: '' }
    ]
    return {
      headers,
      dateTimeHM,
      getUserFullName,
      active,
      selectUser,
      additionalHeaders,
      loading,
      periodPrivileges,
      selectPrivileges,
      selectedUser,
      changeGroupUsersPrivileges,
      changeGroupUsersPrivilegesUpdate
    }
  }
})
</script>
