<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.groups.name') }}
  v-row
    template(v-if="period.periodGroups.length")
      v-col(cols="12" md="4" sm="4")
        v-list
          v-list-item-group(v-model="selectedGroup" color="primary")
            v-list-item(
              v-for="item in period.periodGroups"
              :key="item.id"
              :value="item"
            )
              v-list-item-content {{ item.name }}
              delete-menu(
                v-if="period.canChangeGroups"
                :item-name="String($t('dcis.periods.groups.deleteGroup.itemName'))"
                @confirm="deletePeriodGroup({ id: item.id })"
              )
                template(#default="{ on: onMenu }")
                  v-tooltip(bottom)
                    template(#activator="{ on: onTooltip }")
                      v-list-item-action(v-on="{ ...onMenu, ...onTooltip }")
                        v-btn(color="error" icon)
                          v-icon mdi-delete
                    span {{ $t('dcis.periods.groups.deleteGroup.tooltip') }}
      v-divider(vertical)
    v-col(v-bind="period.periodGroups.length ? { md: 8, sm: 6 } : { }" cols="12")
      period-group-privileges(
        v-if="selectedGroup"
        :group="selectedGroup"
        :can-change="period.canChangeGroups"
        :update="changePeriodGroupPrivilegesUpdate"
      )
      v-row(v-else-if="period.canChangeGroups")
        v-col
          add-period-group(:period="period" :update="addPeriodGroupUpdate")
            template(#activator="{ on }")
              v-card.period-groups__card-add(v-on="on" flat)
                v-icon(large) mdi-plus-circle-outline
                .title {{ $t('dcis.periods.groups.addGroup.buttonText') }}
        v-col
          copy-period-groups(:period="period" :update="copyPeriodGroupsUpdate")
            template(#activator="{ on }")
              v-card.period-groups__card-add(v-on="on" flat)
                v-icon(large) mdi-import
                .title {{ $t('dcis.periods.groups.copyGroups.buttonText') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import { inject, PropType, ref, computed, defineComponent, useNuxt2Meta } from '#app'
import { UpdateType, useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodGroupType,
  PeriodType,
  DeletePeriodGroupMutation,
  DeletePeriodGroupMutationVariables, PeriodQuery
} from '~/types/graphql'
import deletePeriodGroupMutation from '~/gql/dcis/mutations/period/delete_period_group.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import PeriodGroupPrivileges, {
  ChangePeriodGroupPrivilegesMutationResult
} from '~/components/dcis/periods/PeriodGroupPrivileges.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import AddPeriodGroup, { AddPeriodGroupMutationResult } from '~/components/dcis/periods/AddPeriodGroup.vue'
import CopyPeriodGroups, { CopyPeriodGroupsMutationResult } from '~/components/dcis/periods/CopyPeriodGroups.vue'

export type DeletePeriodGroupMutationResult = { data: DeletePeriodGroupMutation }

export default defineComponent({
  components: { LeftNavigatorContainer, PeriodGroupPrivileges, AddPeriodGroup, CopyPeriodGroups, DeleteMenu },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.groups.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-groups' }),
        exact: true
      }
    ]))
    const selectedGroup = ref<PeriodGroupType | null | undefined>(null)
    const periodUpdate = inject<UpdateType<PeriodQuery>>('periodUpdate')

    /**
     * Обновление после добавления группы
     * @param cache
     * @param result
     */
    const addPeriodGroupUpdate = (cache: DataProxy, result: AddPeriodGroupMutationResult) => {
      periodUpdate(
        cache,
        result,
        (dataCache, { data: { addPeriodGroup: { errors, periodGroup } } }: AddPeriodGroupMutationResult) => {
          if (!errors.length) {
            dataCache.period.periodGroups = [
              periodGroup,
              ...dataCache.period.periodGroups
            ] as PeriodQuery['period']['periodGroups']
          }
          return dataCache
        })
      return cache
    }

    /**
     * Обновление после копирования групп
     * @param cache
     * @param result
     */
    const copyPeriodGroupsUpdate = (cache: DataProxy, result: CopyPeriodGroupsMutationResult) => {
      periodUpdate(
        cache,
        result,
        (
          dataCache,
          { data: { copyPeriodGroups: { errors, periodGroups } } }: CopyPeriodGroupsMutationResult
        ) => {
          if (!errors.length) {
            dataCache.period.periodGroups = [
              ...dataCache.period.periodGroups,
              ...periodGroups
            ] as PeriodQuery['period']['periodGroups']
          }
          return dataCache
        })
      return cache
    }

    /**
     * Обновление после изменения привилегий группы
     * @param cache
     * @param result
     */
    const changePeriodGroupPrivilegesUpdate = (
      cache: DataProxy,
      result: ChangePeriodGroupPrivilegesMutationResult
    ) => {
      periodUpdate(
        cache,
        result,
        (
          dataCache,
          { data: { changePeriodGroupPrivileges: { errors, privileges } } }: ChangePeriodGroupPrivilegesMutationResult
        ) => {
          if (!errors.length) {
            const group = dataCache.period.periodGroups
              .find(g => g.id === selectedGroup.value.id)
            group.privileges = privileges as PeriodQuery['period']['periodGroups'][0]['privileges']
          }
          return dataCache
        })
      return cache
    }

    /**
     * Удаление группы
     */
    const { mutate: deletePeriodGroup } = useMutation<
      DeletePeriodGroupMutation,
      DeletePeriodGroupMutationVariables
    >(deletePeriodGroupMutation, {
      update: (cache, result) => periodUpdate(
        cache,
        result,
        (
          dataCache,
          { data: { deletePeriodGroup: { errors, deleteId } } }: DeletePeriodGroupMutationResult
        ) => {
          if (!errors.length) {
            dataCache.period.periodGroups = dataCache.period.periodGroups.filter(g => g.id !== deleteId)
            selectedGroup.value = null
          }
          return dataCache
        }
      )
    })

    return {
      bc,
      selectedGroup,
      addPeriodGroupUpdate,
      copyPeriodGroupsUpdate,
      changePeriodGroupPrivilegesUpdate,
      deletePeriodGroup
    }
  }
})
</script>

<style lang="sass">
.period-groups__card-add
  padding: 20px 0
  border: 1px dashed lightgray !important
  display: flex
  text-align: center
  flex-flow: column
</style>
