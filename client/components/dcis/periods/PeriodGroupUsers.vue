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
            :items="privileges"
            hide-default-footer
            disable-pagination
          )
          v-divider
          v-card-actions.d-flex.flex-wrap.justify-center
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
          a(@click="selectUser = item") {{ getUserFullName(item) }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import {
  PeriodGroupType,
  PeriodPrivilegesQuery,
  PeriodPrivilegesQueryVariables,
  PeriodType,
  UserType
} from '~/types/graphql'
import { useCommonQuery, useFilters, useI18n } from '~/composables'
import periodPrivilegesQuery from '~/gql/dcis/queries/user_privileges.graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import AddPeriodGroupUsers from '~/components/dcis/periods/AddPeriodGroupUsers.vue'
import PeriodGroupPrivileges from '~/components/dcis/periods/PeriodGroupPrivileges.vue'

export default defineComponent({
  components: { AvatarDialog, AddPeriodGroupUsers, PeriodGroupPrivileges },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    periodGroup: {
      type: Object as PropType<PeriodGroupType>,
      default: null
    }
  },
  setup (props) {
    const { dateTimeHM, getUserFullName } = useFilters()
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
    const { data: privileges, loading } = useCommonQuery<PeriodPrivilegesQuery, PeriodPrivilegesQueryVariables>({
      document: periodPrivilegesQuery,
      variables: { userId: selectUser.value?.id, periodId: props.period.id },
      options: { enabled: active.value }
    })
    const additionalHeaders = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.privileges.name') as string, value: 'privilege.name' },
      { text: t('dcis.periods.privileges.key') as string, value: 'privilege.key' }
    ]))
    const headers: DataTableHeader[] = [
      { text: 'Аватар', value: 'avatar' },
      { text: 'ФИО', value: 'name' },
      { text: 'Должность', value: '' },
      { text: 'Участие в других сборах', value: '' }
    ]
    return {
      headers,
      dateTimeHM,
      getUserFullName,
      active,
      selectUser,
      additionalHeaders,
      privileges,
      loading
    }
  }
})
</script>
