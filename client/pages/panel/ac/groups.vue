<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')"  fluid)
  template(#header) {{ $t('panel.groups') }}
  v-row
    v-col(cols="12" md="4")
      v-row(no-gutters align="center")
        v-col(cols="12" md="8").caption {{ $t('panel.ac.groups.name') }}
        v-col.text-right(cols="12" md="4")
          add-group-dialog
      v-list
        v-list-item-group(v-model="selectGroup" color="primary")
          v-list-item(v-for="group in groups" :key="group.id")
            v-list-item-content {{ group.name }} ({{ group.id }})
            v-list-item-action(v-if="hasPerm('auth.change_group')")
              text-menu(:value="group.name" @update="changeGroupName(group, $event)")
                template(v-slot:default="{ on: onMenu }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on: onTooltip }")
                      v-btn(@click.stop="" v-on="{ ...onMenu, ...onTooltip }" icon)
                        v-icon mdi-pencil
                    span {{ $t('panel.ac.groups.change') }}
            v-list-item-action(v-if="hasPerm('auth.delete_group')")
              delete-menu(@confirm="deleteGroupMutate({ groupId: Number(group.id) }).then")
                template(v-slot:default="{ on: onMenu }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on: onTooltip }")
                      v-btn(@click.stop="" v-on="{...onMenu, ...onTooltip}" icon)
                        v-icon mdi-delete
                    span {{ $t('panel.ac.groups.deleteGroup') }}
    v-col(cols="12" md="8")
      .caption {{ $t('panel.ac.permissions.name') }}
      v-row(align="center")
        v-col(cols="12" md="8")
          v-text-field(v-model="searchPermissions" :label="$t('search')" prepend-icon="mdi-magnify")
        v-col.text-right(cols="12" md="4")
          .caption(v-if="selectedGroup") {{ $t('panel.ac.groups.tagged', { count: selectPermissions.length, totalCount: permissions && permissions.length }) }}
      v-data-table(
        :value="selectPermissions"
        @input="changeGroupPermission"
        :search="searchPermissions"
        :headers="permissionHeaders"
        :items="permissions"
        :show-select="selectedGroup"
        dense disable-pagination hide-default-footer)
        template(v-slot:item.contentType="{ item }") {{ item.contentType.appLabel }} / {{ item.contentType.model }}
</template>

<script lang="ts">
import { DataTableHeader } from 'vuetify/types'
import { useMutation } from '@vue/apollo-composable'
import { computed, ComputedRef, defineComponent, PropType, ref, Ref, toRefs, useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import {
  ActionRelationShip,
  ChangeGroupNameMutation,
  ChangeGroupNameMutationVariables,
  ChangeGroupPermissionsMutation,
  ChangeGroupPermissionsMutationVariables,
  DeleteGroupMutation,
  DeleteGroupMutationVariables,
  GroupsQuery,
  GroupsQueryVariables,
  GroupType,
  PermissionsQuery,
  PermissionsQueryVariables,
  PermissionType
} from '~/types/graphql'
import { useAuthStore } from '~/stores'
import { useCommonQuery, useI18n } from '~/composables'
import groupsQuery from '~/gql/core/queries/groups.graphql'
import permissionsQuery from '~/gql/core/queries/permissions.graphql'
import deleteGroup from '~/gql/core/mutations/group/delete_group.graphql'
import changeNameGroupMutation from '~/gql/core/mutations/group/change_group_name.graphql'
import changeGroupPermissionMutation from '~/gql/core/mutations/group/change_group_permissions.graphql'
import AddGroupDialog from '~/components/panel/AddGroupDialog.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import TextMenu from '~/components/common/menu/TextMenu.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { AddGroupDialog, TextMenu, DeleteMenu, LeftNavigatorContainer },
  middleware: 'auth',
  permissions: 'auth.view_group',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('panel.groups') as string })

    const userStore = useAuthStore()
    const { hasPerm } = toRefs(userStore)

    const { data: permissions } = useCommonQuery<PermissionsQuery, PermissionsQueryVariables>({
      document: permissionsQuery
    })
    const { data: groups, update, changeUpdate, deleteUpdate } = useCommonQuery<GroupsQuery, GroupsQueryVariables>({
      document: groupsQuery
    })
    const { mutate: ChangeGroupNameMutate } = useMutation<ChangeGroupNameMutation, ChangeGroupNameMutationVariables>(
      changeNameGroupMutation,
      { update: (cache, result) => changeUpdate(cache, result, 'group') }
    )

    const selectGroup: Ref<number | null | undefined> = ref<number | null | undefined>(null)
    const searchPermissions: Ref<string | null> = ref<string | null>(null)

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: t('panel.groups') as string, to: localePath({ name: 'panel-ac-groups' }), exact: true }
    ]))

    const permissionHeaders: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('panel.ac.groups.tableHeaders.contentType') as string, value: 'contentType' },
      { text: t('panel.ac.groups.tableHeaders.name') as string, value: 'name' },
      { text: t('panel.ac.groups.tableHeaders.codename') as string, value: 'codename' }
    ]))
    const selectPermissions: ComputedRef<PermissionType[]> = computed<PermissionType[]>(():any => {
      if (selectGroup.value === undefined || selectGroup.value === null) { return [] }
      return groups.value[selectGroup.value].permissions
    })

    const selectedGroup: ComputedRef<boolean> = computed<boolean>(() => (
      !(selectGroup.value === undefined || selectGroup.value === null))
    )
    const changeGroupName = (group: GroupType, name: string): void => {
      ChangeGroupNameMutate({ groupId: Number(group.id), name })
    }
    const { mutate: ChangeGroupPermissionMutate } = useMutation<ChangeGroupPermissionsMutation, ChangeGroupPermissionsMutationVariables>(
      changeGroupPermissionMutation,
      {
        update: (cache, result) => update(cache, result,
          (dataCache, { data: { changeGroupPermissions: { success, permissionsId, action } } }): any => {
            if (success) {
              const dataKey: string = Object.keys(dataCache)[0]
              if (action === 'ADD') {
                dataCache[dataKey][selectGroup.value].permissions.push(
                  ...permissions.value.filter(e => permissionsId.includes(Number(e.id)))
                )
              } else if (action === 'DELETE') {
                dataCache[dataKey][selectGroup.value].permissions = dataCache[dataKey][selectGroup.value].permissions.filter(
                  (el: PermissionType) => !permissionsId.includes(Number(el.id))
                )
              }
            }
            return dataCache
          })
      })

    const changeGroupPermission = (permissions: PermissionType[]): void => {
      if (permissions.length === selectPermissions.value.length) { return }
      let diff: PermissionType[]
      let action: string
      if (permissions.length > selectPermissions.value.length) {
        diff = permissions.filter((e: PermissionType) => !selectPermissions.value.map((el: PermissionType) => el.id).includes(e.id))
        action = 'ADD'
      } else {
        diff = selectPermissions.value.filter((e: PermissionType) => !permissions.map((el: PermissionType) => el.id).includes(e.id))
        action = 'DELETE'
      }
      const permissionsId: number[] = diff.map((e: PermissionType) => Number(e.id))
      ChangeGroupPermissionMutate({
        groupId: Number(groups.value[selectGroup.value].id),
        permissionsId,
        action: (action as ActionRelationShip)
      })
    }

    // Мутация для удаления группы
    const { mutate: deleteGroupMutate } = useMutation<DeleteGroupMutation, DeleteGroupMutationVariables>(deleteGroup, {
      update: (cache, result) => deleteUpdate(cache, result)
    })

    return {
      hasPerm,
      selectGroup,
      bc,
      permissionHeaders,
      groups,
      permissions,
      selectedGroup,
      selectPermissions,
      searchPermissions,
      changeGroupName,
      deleteGroupMutate,
      changeGroupPermission
    }
  }
})
</script>
