<template lang="pug">
  v-card(flat)
    v-navigation-drawer(
      v-model="active"
      width="30vw"
      app
      right
      bottom
      temporary
    )
      v-card.ma-2.transparent(v-if="selectUser" flat)
        v-card-subtitle.text-h6.text-center Привилегии пользователя {{ getUserFullName(selectUser) }}
        v-divider
        v-card-text(v-if="selectUser")
          v-data-table.transparent(
            :headers="additionalHeaders"
            :items="privileges"
            hide-default-footer
            disable-pagination
          )
          v-divider
          v-card-actions.d-flex.flex-wrap.justify-center
    v-card-actions
      v-btn(color="primary") Добавить пользователей
      v-spacer
      v-btn(class="align-self-center" icon text)
        v-icon mdi-cog
    v-card-text(v-if="value")
      v-data-table(
        :headers="headers"
        :items="value.users"
        :loading="loading"
        disable-pagination
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
import { PeriodGroupType, PeriodPrivilegesQuery, PeriodPrivilegesQueryVariables, PeriodType, UserType } from '~/types/graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import { useFilters, useI18n, useCommonQuery } from '~/composables'
import periodPrivilegesQuery from '~/gql/dcis/queries/period_privileges.graphql'

export default defineComponent({
  components: { AvatarDialog },
  middleware: 'auth',
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    value: {
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
    const { data: privileges, loading, variables } = useCommonQuery<PeriodPrivilegesQuery, PeriodPrivilegesQueryVariables>({
      document: periodPrivilegesQuery,
      variables: { userId: '', periodId: '' }
    })
    const selectedUser = (id: string): void => {
      variables.value = { userId: id, periodId: props.period.id }
      selectUser.value = props.value.users.find(user => user.id === id)
    }
    const additionalHeaders = computed<DataTableHeader[]>(() => ([
      { text: t('dcis.periods.groups.name') as string, value: 'privilege.name' },
      { text: t('dcis.periods.groups.key') as string, value: 'privilege.key' }
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
      loading,
      selectedUser
    }
  }
})
</script>
