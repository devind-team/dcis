<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) {{ $t('dcis.periods.users.name') }}
      template(v-if="period.canChangeUsers")
        v-spacer
        v-btn(color="primary") {{ $t('dcis.periods.users.addUser.buttonText') }}
    v-row(align="center")
      v-col(cols="12" md="8")
        v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right.pr-5(
        cols="12"
        md="4"
      ) {{ $t('shownOf', { count: userCount, totalCount: users.length }) }}
    v-card(flat)
      v-card-text
        v-data-table(
          :headers="headers"
          :items="users"
          :search="search"
          disable-pagination
          hide-default-footer
          @pagination="pagination"
        )
          template(#item.avatar="{ item }")
            avatar-dialog(:item="item")
          template(#item.actions="{ item }")
            v-tooltip(bottom)
              template(#activator="{ on }")
                v-btn(v-on="on" color="success" icon)
                  v-icon mdi-book-edit
              span {{ $t('dcis.periods.users.tooltips.changeGroups') }}
            v-tooltip(bottom)
              template(#activator="{ on }")
                v-btn(v-on="on" color="success" icon)
                  v-icon mdi-clipboard-edit
              span {{ $t('dcis.periods.users.tooltips.changePrivileges') }}
</template>

<script lang="ts">
import { DataTableHeader, DataPagination } from 'vuetify'
import { computed, PropType } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import {
  UserType,
  UserFieldsFragment,
  PeriodType,
  PeriodUsersQuery,
  PeriodQueryVariables
} from '~/types/graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import periodUsers from '~/gql/dcis/queries/period_users.graphql'

type ExtendedUserType = UserFieldsFragment & { fullname: string }

export default defineComponent({
  components: { LeftNavigatorContainer, AvatarDialog },
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

    const { data: usersData, loading: usersLoading } = useCommonQuery<PeriodUsersQuery, PeriodQueryVariables>({
      document: periodUsers,
      variables: () => ({
        periodId: props.period.id
      })
    })
    const users = computed<ExtendedUserType[]>(() =>
      usersData.value
        ? usersData.value.map(user => ({ ...user, fullname: getUserFullName(user as UserType) }))
        : []
    )

    const { search } = useDebounceSearch()
    const userCount = ref<number>(0)
    const pagination = (pagination: DataPagination) => {
      userCount.value = pagination.itemsLength
    }

    return {
      getUserFullName,
      bc,
      headers,
      usersLoading,
      users,
      search,
      userCount,
      pagination
    }
  }
})
</script>
