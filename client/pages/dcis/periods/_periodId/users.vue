<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) {{ period.name }}
    v-row
      template(v-if="period.periodGroups.length")
        v-col(cols="12" md="4" sm="4")
          v-row
            v-subheader Группы
          v-list
            v-list-item-group(v-model="selectGroup" color="primary")
              v-list-item(
                v-for="item in period.periodGroups"
                :key="item.id"
                :value="item"
              )
                v-list-item-content {{ item.name }}
                delete-menu(@confirm="deletePeriodGroupMutate({ id: item.id })")
                  template(#default="{ on }")
                    v-list-item-action(v-on="on")
                      v-btn(icon)
                        v-icon mdi-delete
        v-divider(vertical)
      v-col(v-bind="period.periodGroups.length ? { md: 8, sm: 6 } : { }" cols="12")
        period-group-users(v-if="selectGroup" :period-group="selectGroup" :period="period" :update="deleteUserFromPeriodGroupUpdate")
        v-row(v-else)
          v-col
            add-period-group(:period="period" :update="addPeriodGroupUpdate")
              template(#activator="{ on }")
                v-card.period-users-card-add(v-on="on" flat)
                  v-icon(large) mdi-plus-circle-outline
                  .title {{ $t('dcis.periods.actions.addGroup') }}
          v-col
            copy-period-groups(:period="period" active-query)
              template(#activator="{ on }")
                v-card.period-users-card-add(v-on="on" flat)
                  v-icon(large) mdi-import
                  .title {{ $t('dcis.periods.actions.copyGroups') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import { ComputedRef, inject, PropType, ref, provide, computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodGroupType,
  PeriodType,
  DeletePeriodGroupMutation,
  DeletePeriodGroupMutationVariables,
  UserType
} from '~/types/graphql'
import deletePeriodGroup from '~/gql/dcis/mutations/project/delete_period_group.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import PeriodGroupUsers, { DeleteUserFromPeriodGroupMutationResult } from '~/components/dcis/periods/PeriodGroupUsers.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import AddPeriodGroup, { AddPeriodGroupMutationResult } from '~/components/dcis/periods/AddPeriodGroup.vue'
import CopyPeriodGroups, { CopyPeriodGroupsMutationResult } from '~/components/dcis/periods/CopyPeriodGroups.vue'
import { ChangePeriodGroupUsersMutationResult } from '~/components/dcis/periods/AddPeriodGroupUsers.vue'
import { ChangePeriodGroupPrivilegesMutationResult } from '~~/components/dcis/periods/PeriodGroupPrivileges.vue'

export type DeletePeriodGroupMutationResult = { data: DeletePeriodGroupMutation }

export default defineComponent({
  components: { LeftNavigatorContainer, PeriodGroupUsers, AddPeriodGroup, CopyPeriodGroups, DeleteMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Пользователи', to: localePath({ name: 'dcis-periods-periodId-users' }), exact: true }
    ]))
    const selectGroup = ref<PeriodGroupType | null | undefined>(null)
    const periodUpdate: any = inject('periodUpdate')

    /**
     *  Обновление после добавления группы
     * @param cache
     * @param result
     */
    const addPeriodGroupUpdate = (cache: DataProxy, result: AddPeriodGroupMutationResult) => {
      periodUpdate(cache, result, (dataCache, { data: { addPeriodGroup: { errors, periodGroup } } }: AddPeriodGroupMutationResult) => {
        if (!errors.length) {
          dataCache.period.periodGroups = [periodGroup, ...dataCache.period.periodGroups]
        }
        return dataCache
      })
    }

    /**
     * Обновление после добавления пользователей
     * @param cache
     * @param result
     */
    const changePeriodGroupUsersUpdate = (cache: DataProxy, result: ChangePeriodGroupUsersMutationResult) => {
      periodUpdate(
        cache, result, (dataCache, { data: { changePeriodGroupUsers: { errors, users } } }: ChangePeriodGroupUsersMutationResult
        ) => {
          if (!errors.length) {
            dataCache.period.periodGroups.find((e: any) => e.id === selectGroup.value.id).users = users
          }
          return dataCache
        })
    }

    /**
     *  Обновление после добавления групп из другого сбора
     * @param cache
     * @param result
     */
    const copyPeriodGroupsUpdate = (cache: DataProxy, result: CopyPeriodGroupsMutationResult) => {
      periodUpdate(
        cache, result, (dataCache, { data: { copyPeriodGroups: { success, periodGroups } } }: CopyPeriodGroupsMutationResult
        ) => {
          if (success) {
            dataCache.period.periodGroups.push(...periodGroups)
          }
          return dataCache
        })
    }

    /**
     * Обновление после изменения привилегий группы
     * @param cache
     * @param result
     */
    const changePeriodGroupPrivilegesUpdate = (cache: DataProxy, result: ChangePeriodGroupPrivilegesMutationResult) => {
      periodUpdate(
        cache, result, (dataCache, { data: { changePeriodGroupPrivileges: { errors, privileges } } }: ChangePeriodGroupPrivilegesMutationResult
        ) => {
          if (!errors.length) {
            const periodGroup: any = dataCache.period.periodGroups.find((e: any) => e.id === selectGroup.value.id)
            periodGroup.privileges = privileges
          }
          return dataCache
        })
    }

    /**
     * Обновление после удаления группы
     */
    const { mutate: deletePeriodGroupMutate } = useMutation<DeletePeriodGroupMutation, DeletePeriodGroupMutationVariables>(deletePeriodGroup, {
      update: (cache, result) => periodUpdate(
        cache,
        result,
        (dataCache, { data: { deletePeriodGroup: { errors, deletedId } } }: DeletePeriodGroupMutationResult) => {
          if (!errors.length) {
            dataCache.period.periodGroups = dataCache.period.periodGroups.filter((e: any) => e.id !== deletedId)
            selectGroup.value = null
          }
          return dataCache
        }
      )
    })

    /**
     * Обновление после удаления пользователя из группы
     * @param cache
     * @param result
     */
    const deleteUserFromPeriodGroupUpdate = (cache: DataProxy, result: DeleteUserFromPeriodGroupMutationResult) => {
      periodUpdate(
        cache, result, (dataCache, { data: { deleteUserFromPeriodGroup: { errors, id } } }: DeleteUserFromPeriodGroupMutationResult
        ) => {
          if (!errors.length) {
            const selectedPeriodGroup: any = dataCache.period.periodGroups.find((e: PeriodGroupType) => e.id === selectGroup.value.id)
            selectedPeriodGroup.users = selectedPeriodGroup.users.filter((e: UserType) => e.id !== id)
          }
          return dataCache
        })
    }

    provide('periodGroupUsersUpdate', changePeriodGroupUsersUpdate)
    provide('periodGroupPrivilegesUpdate', changePeriodGroupPrivilegesUpdate)
    provide('copyPeriodGroupsUpdate', copyPeriodGroupsUpdate)

    return {
      bc,
      selectGroup,
      addPeriodGroupUpdate,
      changePeriodGroupUsersUpdate,
      changePeriodGroupPrivilegesUpdate,
      deletePeriodGroupMutate,
      deleteUserFromPeriodGroupUpdate
    }
  }
})
</script>

<style lang="sass">
.period-users-card-add
  padding: 20px 0
  border: 1px dashed lightgray !important
  display: flex
  text-align: center
  flex-flow: column
</style>
