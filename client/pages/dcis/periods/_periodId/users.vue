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
              v-list-item-title {{ item.name }}
      v-divider(vertical)
      v-col(cols="12" md="8" sm="8")
        period-group-users(:period-group="selectGroup" :period="period")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { ComputedRef, inject, PropType, ref, provide } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodGroupType, PeriodType } from '~/types/graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import PeriodGroupUsers from '~/components/dcis/periods/PeriodGroupUsers.vue'
import AddPeriodGroup, { AddPeriodGroupMutationResult } from '~/components/dcis/periods/AddPeriodGroup.vue'
import { ChangePeriodGroupMutationResult } from '~/components/dcis/periods/AddPeriodGroupUsers.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, PeriodGroupUsers, AddPeriodGroup },
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

    const addPeriodGroupUpdate = (cache: DataProxy, result: AddPeriodGroupMutationResult) => {
      periodUpdate(cache, result, (dataCache, { data: { addPeriodGroup: { errors, periodGroup } } }: AddPeriodGroupMutationResult) => {
        if (!errors.length) {
          dataCache.period.periodGroups = [periodGroup, ...dataCache.period.periodGroups]
        }
        return dataCache
      })
    }
    const changePeriodGroupUsersUpdate = (cache: DataProxy, result: ChangePeriodGroupMutationResult) => {
      periodUpdate(cache, result, (dataCache, { data: { changePeriodGroup: { errors, periodGroup } } }: ChangePeriodGroupMutationResult) => {
        if (!errors.length) {
          const index: number = dataCache.period.periodGroups.findIndex((e: any) => e.id === periodGroup.id)
          dataCache.period.periodGroups.splice(index, 1, periodGroup)
          selectGroup.value = periodGroup
        }
        return dataCache
      })
    }
    provide('periodGroupUpdate', changePeriodGroupUsersUpdate)
    return { bc, selectGroup, addPeriodGroupUpdate, changePeriodGroupUsersUpdate }
  }
})
</script>
