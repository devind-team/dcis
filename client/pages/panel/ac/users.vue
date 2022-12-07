<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('panel.ac.users.name') }}
  v-row(align="center")
    v-col(cols="12" md="6")
      add-users-menu(v-if="hasPerm('core.add_user')" :update="updateUsers")
        template(#default="{ on }")
          v-btn(v-on="on" color="primary")
            v-icon(left) mdi-account-multiple-plus
            | {{ $t('panel.ac.users.addUsers') }}
    v-col.text-right(cols="12" md="6")
      unload-users-menu
        template(#default="{ on }")
          v-btn(v-on="on" color="success" @click="")
            v-icon(left) mdi-upload
            | {{ $t('panel.ac.users.unloadUsers') }}
  v-row(align="center")
    v-col(cols="12" md="6")
      v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
    v-col.caption.text-right(cols="12" md="6") {{ $t('shownOf', { count, totalCount }) }}
  v-data-table(
    :headers="headers"
    :items="extendedUsers"
    :loading="loading"
    hide-default-footer
    disable-pagination
  )
    template(#item.avatar="{ item }")
      avatar-dialog(:item="item")
    template(#item.groups="{ item }")
      change-group-dialog(
        :user="item"
        :groups="groups"
        @update="args => updateGroups(item, ...args)"
      )
        template(#default="{ on: onDialog }")
          v-tooltip(bottom)
            template(#activator="{ on: onTooltip }")
              div(
                v-on="{ ...onDialog, ...onTooltip }"
                style="cursor: pointer"
              ) {{ item.groups.length ? item.groups.map(e => e.name).join(', ') : $t('panel.ac.users.changeGroups.noGroups') }}
            span {{ $t('panel.ac.users.change') }}
    template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify/types'
import { DataProxy } from 'apollo-cache'
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import {
  UserType,
  UsersQueryVariables,
  GroupsQuery,
  GroupsQueryVariables,
  UsersQuery,
  UserTypeEdge,
  ChangeUserGroupsMutationPayload,
  UploadUsersMutationPayload,
  GroupType
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import { useAuthStore } from '~/stores'
import { useCommonQuery, useCursorPagination, useDebounceSearch, useI18n, useQueryRelay, useFilters } from '~/composables'
import usersQuery from '~/gql/core/queries/users.graphql'
import groupsQuery from '~/gql/core/queries/groups.graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import TwoColumns from '~/components/common/grid/TwoColumns.vue'
import ChangeGroupDialog from '~/components/panel/ChangeGroupDialog.vue'
import AddUsersMenu from '~/components/users/AddUsersMenu.vue'
import UnloadUsersMenu from '~/components/users/UnloadUsersMenu.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

type ChangeUserGroupsData = { data: { changeUserGroups: ChangeUserGroupsMutationPayload } }
type UploadUsersData = { data: { uploadUsers: UploadUsersMutationPayload } }

export default defineComponent({
  components: {
    AvatarDialog,
    UnloadUsersMenu,
    AddUsersMenu,
    ChangeGroupDialog,
    LeftNavigatorContainer,
    TwoColumns,
    BreadCrumbs
  },
  middleware: 'auth',
  permissions: 'core.view_user',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.ac.users.name') as string })
    const { dateTimeHM, getUserFullName } = useFilters()

    const { hasPerm } = useAuthStore()

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('panel.ac.users.name') as string, to: localePath({ name: 'panel-ac-users' }), exact: true }
    ]))

    const headers = computed<DataTableHeader[]>(() => ([
      { text: t('panel.ac.users.tableHeaders.avatar') as string, value: 'avatar', align: 'center', sortable: false },
      { text: t('panel.ac.users.tableHeaders.name') as string, value: 'fullName' },
      { text: t('panel.ac.users.tableHeaders.username') as string, value: 'username' },
      { text: t('panel.ac.users.tableHeaders.email') as string, value: 'email' },
      { text: t('panel.ac.users.tableHeaders.groups') as string, value: 'groups' },
      { text: t('panel.ac.users.tableHeaders.createdAt') as string, value: 'createdAt' }
    ]))

    const { data: groups } = useCommonQuery<GroupsQuery, GroupsQueryVariables>({
      document: groupsQuery
    })

    const { search, debounceSearch } = useDebounceSearch()
    const {
      loading,
      pagination: { count, totalCount },
      data: users,
      update
    } = useQueryRelay<UsersQuery, UsersQueryVariables, UserType>({
      document: usersQuery,
      variables: () => ({
        search: debounceSearch.value
      })
    }, {
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    const extendedUsers = computed(() => {
      if (!users.value) {
        return []
      }
      return users.value.map((user: UserType) => ({
        ...user,
        fullName: getUserFullName(user)
      })
      )
    })

    /**
     * Обновление групп пользователя после изменения
     * @param user - выбранный пользователь
     * @param cache - кеш
     * @param result - результат мутации
     */
    const updateGroups = (
      user: UserType,
      cache: DataProxy,
      result: ChangeUserGroupsData
    ) => {
      const { data: { changeUserGroups: { success } } } = result
      if (success) {
        update(cache, result, (dataCache, { data: { changeUserGroups: { groups } } }) => {
          dataCache.users.edges
            .find((u: UserTypeEdge | any) => u.node.id === user.id).node
            .groups = groups as Required<Pick<GroupType, '__typename' | 'id' | 'name'>>[]
          return dataCache
        })
      }
    }

    /**
     * Обновление пользователей после добавления нового пользователя
     * @param cache - кеш
     * @param result - результат мутации
     */
    const updateUsers = (cache: DataProxy, result: UploadUsersData) => {
      const { data: { uploadUsers: { success } } } = result
      if (success) {
        update(cache, result, (dataCache, { data: { uploadUsers: { users } } }) => {
          dataCache.users.totalCount += users.length
          dataCache.users.edges = [
            ...users!.map(user => ({ node: user, __typename: 'UserTypeEdge' })).reverse(),
            ...dataCache.users.edges
          ] as typeof dataCache.users.edges
          return dataCache
        })
      }
    }

    return {
      hasPerm,
      dateTimeHM,
      getUserFullName,
      bc,
      headers,
      groups,
      search,
      loading,
      count,
      totalCount,
      updateGroups,
      updateUsers,
      extendedUsers
    }
  }
})
</script>
