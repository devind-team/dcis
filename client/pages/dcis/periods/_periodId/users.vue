<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) {{ $t('dcis.periods.users.name') }}
      template(v-if="period.canChangeUsers")
        v-spacer
        add-period-user(:period="period" :period-users="periodUsers" :update="addPeriodUserUpdate")
          template(#activator="{ on }")
            v-btn(v-on="on" color="primary") {{ $t('dcis.periods.users.addUser.buttonText') }}
    v-row(align="center")
      v-col(cols="12" md="8")
        v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right.pr-5(
        cols="12"
        md="4"
      ) {{ $t('shownOf', { count: usersCount, totalCount: users.length }) }}
    v-card(flat)
      v-card-text
        v-data-table(
          :headers="headers"
          :items="users"
          :search="search"
          :loading="loading"
          disable-pagination
          hide-default-footer
          @pagination="pagination"
        )
          template(#item.avatar="{ item }")
            avatar-dialog(:item="item")
          template(#item.actions="{ item }")
            change-user-period-groups(:period="period" :user="item" :update="changeUserPeriodGroupsUpdate")
              template(#activator="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{ ...onMenu, ...onTooltip }" color="success" icon)
                      v-icon mdi-book-edit
                  span {{ $t('dcis.periods.users.changeGroups.tooltip') }}
            change-user-period-privileges(:period="period" :user="item")
              template(#activator="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{ ...onMenu, ...onTooltip }" color="success" icon)
                      v-icon mdi-clipboard-edit
                  span {{ $t('dcis.periods.users.changePrivileges.tooltip') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { DataTableHeader, DataPagination } from 'vuetify'
import { PropType, ref } from '#app'
import { UpdateType } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  UserType,
  UserFieldsFragment,
  PeriodType,
  PeriodGroupType,
  PeriodGroupFieldsFragment,
  PeriodQuery,
  PeriodUsersQuery,
  PeriodQueryVariables
} from '~/types/graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import AddPeriodUser, {
  AddPeriodUserMutationResult
} from '~/components/dcis/periods/AddPeriodUser.vue'
import ChangeUserPeriodGroups, {
  ChangeUserPeriodGroupsMutationResult
} from '~/components/dcis/periods/ChangeUserPeriodGroups.vue'
import ChangeUserPeriodPrivileges from '~/components/dcis/periods/ChangeUserPeriodPrivileges.vue'
import periodUsersQuery from '~/gql/dcis/queries/period_users.graphql'

type ExtendedUserType = UserFieldsFragment & { fullname: string }

export default defineComponent({
  components: {
    LeftNavigatorContainer,
    AvatarDialog,
    AddPeriodUser,
    ChangeUserPeriodGroups,
    ChangeUserPeriodPrivileges
  },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { getUserFullName } = useFilters()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.users.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-users' }),
        exact: true
      }
    ]))

    const headers = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = [
        {
          text: t('dcis.periods.users.tableHeaders.avatar') as string,
          value: 'avatar',
          align: 'center',
          sortable: false,
          filterable: false
        },
        { text: t('dcis.periods.users.tableHeaders.fullname') as string, value: 'fullname' },
        { text: t('dcis.periods.users.tableHeaders.username') as string, value: 'username' },
        { text: t('dcis.periods.users.tableHeaders.email') as string, value: 'email' }
      ]
      if (props.period.canChangeUsers) {
        result.push({
          text: t('dcis.periods.users.tableHeaders.actions') as string,
          value: 'actions',
          align: 'center',
          sortable: false,
          filterable: false
        })
      }
      return result
    })

    const { data: periodUsers, loading, update: periodUsersUpdate } = useCommonQuery<
      PeriodUsersQuery,
      PeriodQueryVariables
    >({
      document: periodUsersQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })
    const users = computed<ExtendedUserType[]>(() =>
      periodUsers.value
        ? periodUsers.value.map(user => ({ ...user, fullname: getUserFullName(user as UserType) }))
        : []
    )

    const search = ref<string>('')
    const usersCount = ref<number>(0)
    const pagination = (pagination: DataPagination) => {
      usersCount.value = pagination.itemsLength
    }

    const periodUpdate: UpdateType<PeriodQuery> = inject('periodUpdate')

    const changeUserPeriodGroupsUpdate = (
      cache: DataProxy,
      result: ChangeUserPeriodGroupsMutationResult
    ) => {
      periodUpdate(
        cache,
        result,
        (
          dataCache,
          { data: { changeUserPeriodGroups: { errors, user, periodGroups } } }: ChangeUserPeriodGroupsMutationResult
        ) => {
          if (!errors.length) {
            for (const periodGroup of dataCache.period.periodGroups) {
              const isUserPeriodGroup = !!periodGroups.find((group: PeriodGroupType) => group.id === periodGroup.id)
              if (isUserPeriodGroup) {
                if (!periodGroup.users.find((u: UserFieldsFragment) => u.id === user.id)) {
                  periodGroup.users.push(user as UserFieldsFragment)
                }
              } else {
                periodGroup.users = periodGroup.users.filter((u: UserFieldsFragment) => u.id !== user.id)
              }
            }
          }
          return dataCache
        })
      return cache
    }

    const addPeriodUserUpdate = (
      cache: DataProxy,
      result: AddPeriodUserMutationResult
    ) => {
      if (!result.data.changeUserPeriodGroups.errors.length && !result.data.changeUserPeriodPrivileges.errors.length) {
        periodUsersUpdate(
          cache,
          result,
          (
            dataCache,
            { data: { changeUserPeriodGroups: { user } } }
          ) => {
            dataCache.periodUsers.push(user as UserFieldsFragment)
            dataCache.periodUsers.sort((u1: UserFieldsFragment, u2: UserFieldsFragment) =>
              new Date(u2.createdAt).getTime() - new Date(u1.createdAt).getTime()
            )
            return dataCache
          }
        )
        periodUpdate(
          cache,
          result,
          (
            dataCache,
            { data: { changeUserPeriodGroups: { user, periodGroups } } }
          ) => {
            for (const userPeriodGroup of periodGroups) {
              const periodGroup = dataCache.period.periodGroups.find((periodGroup: PeriodGroupFieldsFragment) =>
                periodGroup.id === userPeriodGroup.id
              )
              periodGroup.users.push(user as UserFieldsFragment)
            }
            return dataCache
          }
        )
      }
      return cache
    }

    return {
      getUserFullName,
      bc,
      headers,
      loading,
      periodUsers,
      users,
      search,
      usersCount,
      pagination,
      changeUserPeriodGroupsUpdate,
      addPeriodUserUpdate
    }
  }
})
</script>
