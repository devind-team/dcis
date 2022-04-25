<template lang="pug">
  v-menu(bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-list
      mutation-modal-form(
        :header="String($t('dcis.periods.changePeriodGroupPrivileges.header'))"
        :button-text="String($t('dcis.periods.changePeriodGroupPrivileges.buttonText'))"
        :mutation="changePeriodGroup"
        :variables="{ periodGroupId: periodGroup.id, privilegesIds: selectedPrivileges.map(e => e.id) }"
        mutation-name="changePeriodGroup"
        errors-in-alert
        persistent
      )
        template(#activator="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-pencil
            v-list-item-title Изменить привилегии группы
        template(#form)
          v-data-table(
            v-model="selectedPrivileges"
            :headers="headers"
            :items="privileges"
            show-select
            hide-default-footer
          )
</template>

<script lang="ts">
import type { PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { defineComponent, computed } from '#app'
import { PeriodGroupType, PrivilegesQuery, PrivilegesQueryVariables, PrivilegeType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useCommonQuery } from '~/composables'
import privilegesQuery from '~/gql/dcis/queries/privileges.graphql'
import changePeriodGroup from '~/gql/dcis/mutations/project/change_period_group.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    periodGroup: { type: Object as PropType<PeriodGroupType>, required: true }
  },
  setup (props) {
    const { data: privileges, loading } = useCommonQuery<PrivilegesQuery, PrivilegesQueryVariables>({
      document: privilegesQuery
    })
    const selectedPrivileges = computed<PrivilegeType[]>({
      get: () => (props.periodGroup.privileges),
      set: (value: PrivilegeType[]) => console.log(privileges.value.filter(item => value.map(e => e.id).includes(item.id)))
    })
    const headers: DataTableHeader[] = [
      { text: 'Описание привилегии', value: 'name' },
      { text: 'Ключ', value: 'key' }
    ]
    return { headers, privileges, loading, selectedPrivileges, changePeriodGroup }
  }
})
</script>
