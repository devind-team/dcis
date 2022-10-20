<template lang="pug">
v-dialog(v-model="active" width="600px" persistent scrollable)
  template(#activator="{ on }")
    div(v-on="on") {{ value }}
  v-card
    v-card-title {{ t('dcis.grid.changeValue') }}
      v-spacer
      v-btn(@click="cancel" icon)
        v-icon mdi-close
    v-card-text(style="height: 60vh")
      v-list
        v-list-item(v-for="department in departments" :key="department.id" @click="setValue(department)")
          v-list-item-content
            v-list-item-title {{ department.code }} {{ department.name }}
</template>

<script lang="ts">
import type { Ref } from '#app'
import { defineComponent, ref } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { DepartmentsQuery, DepartmentsQueryVariables, DepartmentFieldFragment } from '~/types/graphql'
import departmentQuery from '~/gql/dcis/queries/departments.graphql'

export default defineComponent({
  props: {
    value: { type: String, default: null }
  },
  setup (_, { emit }) {
    const { t } = useI18n()

    const active: Ref<boolean> = ref<boolean>(true)

    const { data: departments } = useCommonQuery<DepartmentsQuery, DepartmentsQueryVariables, 'departments'>({
      document: departmentQuery
    })

    const setValue = (department: DepartmentFieldFragment) => {
      active.value = false
      const value: string = department.code ? `${department.code} ${department.name}` : department.name
      emit('set-value', value)
    }

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    return { t, active, departments, setValue, cancel }
  }
})
</script>
