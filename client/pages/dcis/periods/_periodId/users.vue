<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) {{ period.name }}
    v-row
      v-col(cols="12" md="4" sm="4")
        v-list
          v-list-item-group(v-model="selectGroup" color="primary")
            v-row(no-gutters align="center")
              v-col(cols="12" md="4" sm="2")
                v-subheader Группы
              v-col.text-right(cols="12" md="8" sm="10")
                add-period-group(:period="period" :update="addPeriodGroupUpdate")
                  template(#activator="{ on }")
                    v-btn(v-on="on" class="align-self-center mr-4" color="primary" icon text)
                      v-icon(large) mdi-plus-circle
            v-list-item(
              v-for="(item, index) in period.periodGroups"
              :key="index"
              :value="item"
            )
              v-list-item-content {{ item.name }}
              v-list-item-action
                delete-menu(@confirm="deletePeriodGroupMutate({ id: Number(item.id) }).then()")
                  template(v-slot:default="{ on: onMenu }")
                    v-tooltip(bottom)
                      template(v-slot:activator="{ on: onTooltip }")
                        v-hover(v-slot="{ hover }")
                          v-btn(:color="hover ? 'error' : ''" @click.stop="" v-on="{...onMenu, ...onTooltip}" icon)
                            v-icon mdi-delete
                      span {{ $t('dcis.periods.actions.deleteGroup') }}
      v-divider(vertical)
      v-col(cols="12" md="8" sm="8")
        period-group-users(:period-group="selectGroup" :period="period" :update="deleteUserFromPeriodGroupUpdate")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import { ComputedRef, inject, PropType, ref, provide, computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodGroupType, PeriodType, DeletePeriodGroupMutation, DeletePeriodGroupMutationVariables } from '~/types/graphql'
import deletePeriodGroup from '~/gql/dcis/mutations/project/delete_period_group.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import PeriodGroupUsers, { DeleteUserFromPeriodGroupMutationResult } from '~/components/dcis/periods/PeriodGroupUsers.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import AddPeriodGroup, { AddPeriodGroupMutationResult } from '~/components/dcis/periods/AddPeriodGroup.vue'
import { ChangePeriodGroupUsersMutationResult } from '~/components/dcis/periods/AddPeriodGroupUsers.vue'
import { ChangePeriodGroupPrivilegesMutationResult } from '~~/components/dcis/periods/PeriodGroupPrivileges.vue'

export type DeletePeriodGroupMutationResult = { data: DeletePeriodGroupMutation }

export default defineComponent({
  components: { LeftNavigatorContainer, PeriodGroupUsers, AddPeriodGroup, DeleteMenu },
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

    // Обновление после добавления группы
    const addPeriodGroupUpdate = (cache: DataProxy, result: AddPeriodGroupMutationResult) => {
      periodUpdate(cache, result, (dataCache, { data: { addPeriodGroup: { errors, periodGroup } } }: AddPeriodGroupMutationResult) => {
        if (!errors.length) {
          dataCache.period.periodGroups = [periodGroup, ...dataCache.period.periodGroups]
        }
        return dataCache
      })
    }

    // Обновление после добавления пользователей
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

    // Обновление после изменения привилегий группы
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

    // Обновление после удаления группы
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

    // Обновление после удаления пользователя из группы
    const deleteUserFromPeriodGroupUpdate = (cache: DataProxy, result: DeleteUserFromPeriodGroupMutationResult) => {
      periodUpdate(
        cache, result, (dataCache, { data: { deleteUserFromPeriodGroup: { errors, id } } }: DeleteUserFromPeriodGroupMutationResult
        ) => {
          if (!errors.length) {
            const selectedPeriodGroup: any = dataCache.period.periodGroups.find((e: any) => e.id === selectGroup.value.id)
            selectedPeriodGroup.users = selectedPeriodGroup.users.filter((e: any) => e.id !== id)
          }
          return dataCache
        })
    }

    provide('periodGroupUsersUpdate', changePeriodGroupUsersUpdate)
    provide('periodGroupPrivilegesUpdate', changePeriodGroupPrivilegesUpdate)

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
