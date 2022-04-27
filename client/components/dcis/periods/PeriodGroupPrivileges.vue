<template lang="pug">
  v-menu(v-model="active" bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-list
      mutation-modal-form(
        :header="String($t('dcis.periods.changePeriodGroupPrivileges.header', { groupName }))"
        :button-text="String($t('dcis.periods.changePeriodGroupPrivileges.buttonText'))"
        :mutation="changePeriodGroupPrivileges"
        :update="changePeriodGroupPrivilegesUpdate"
        :variables="{ periodGroupId: periodGroup.id, privilegesIds: selectPrivileges.map(e => e.id) }"
        mutation-name="changePeriodGroupPrivileges"
        errors-in-alert
        persistent
        @done="done"
      )
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-pencil
            v-list-item-title Изменить привилегии группы
        template(#form)
          v-data-table(
            v-model="selectPrivileges"
            :headers="headers"
            :items="privileges"
            :loading="loading"
            item-key="id"
            show-select
            hide-default-footer
          )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, inject, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import {
  ChangePeriodGroupPrivilegesMutationPayload,
  PeriodGroupType,
  PrivilegesQuery,
  PrivilegesQueryVariables,
  PrivilegeType
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useCommonQuery } from '~/composables'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import changePeriodGroupPrivileges from '~/gql/dcis/mutations/privelege/change_period_group_privileges.graphql'

export type ChangePeriodGroupPrivilegesMutationResult = { data: { changePeriodGroupPrivileges: ChangePeriodGroupPrivilegesMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    periodGroup: { type: Object as PropType<PeriodGroupType>, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)
    const { data: privileges, loading } = useCommonQuery<PrivilegesQuery, PrivilegesQueryVariables>({
      document: privilegesQuery,
      options: { enabled: active }
    })
    const groupName = ref<string>(props.periodGroup.name)
    const selectPrivileges = ref<PrivilegeType[]>(props.periodGroup.privileges)
    const headers: DataTableHeader[] = [
      { text: 'Описание привилегии', value: 'name' },
      { text: 'Ключ', value: 'key' }
    ]
    const done = (result: any): void => {
      emit('input', result.data.changePeriodGroupPrivileges.privileges)
      nextTick(() => { selectPrivileges.value = props.periodGroup.privileges })
    }
    const periodGroupPrivilegesUpdate: any = inject('periodGroupPrivilegesUpdate')
    const changePeriodGroupPrivilegesUpdate = (cache: DataProxy, result: ChangePeriodGroupPrivilegesMutationResult) => {
      const { success } = result.data.changePeriodGroupPrivileges
      if (success) {
        periodGroupPrivilegesUpdate(cache, result)
      }
    }
    return { headers, privileges, loading, changePeriodGroupPrivileges, groupName, selectPrivileges, done, active, changePeriodGroupPrivilegesUpdate }
  }
})
</script>
