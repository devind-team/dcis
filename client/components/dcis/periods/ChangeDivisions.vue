<template lang="pug">
  mutation-modal-form(
    @close="close"
    :header="String($t('dcis.periods.divisions.formHeader'))"
    :button-text="String($t('dcis.periods.divisions.buttonText'))"
    :mutation="changeDivisions"
    :update="changeDivisionsUpdate"
    :variables="{ periodId: period.id, divisionIds: selectedDivisions.map(e => e.id) }"
    width="50vw"
    mutation-name="changeDivisions"
    errors-in-alert
    persistent
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      v-text-field(v-model="search" :placeholder="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-data-table(
        v-model="selectedDivisions"
        :headers="headers"
        :items="divisions"
        :loading="loading"
        :items-per-page="33"
        :search.sync="search"
        item-key="id"
        show-select
        hide-default-footer
      )
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { DataTableHeader } from 'vuetify'
import { DataProxy } from 'apollo-cache'
import { ChangeDivisionsMutationPayload, DepartmentType, OrganizationType, PeriodType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useDebounceSearch, useI18n } from '~/composables'
import changeDivisions from '~/gql/dcis/mutations/project/change_divisions.graphql'

export type ChangeDivisionsMutationResult = { data: { changeDivisions: ChangeDivisionsMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: ChangeDivisionsMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    divisions: { type: Array as PropType<any>, default: () => [] },
    loading: { type: Boolean as PropType<boolean>, default: false },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const { search } = useDebounceSearch()
    const divisionsListId = ref<string[]>([])
    const selectedDivisions = ref<DepartmentType[] | OrganizationType[]>([])
    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.name') as string, value: 'name' }
    ]
    /**
     * Обновление после добавления объектов
     * @param cache
     * @param result
     */
    const changeDivisionsUpdate = (cache: DataProxy, result: ChangeDivisionsMutationResult) => {
      const { success } = result.data.changeDivisions
      if (success) {
        props.update(cache, result)
      }
    }
    const close = () => {
      selectedDivisions.value = []
      search.value = ''
    }
    return { headers, changeDivisions, divisionsListId, search, changeDivisionsUpdate, close, selectedDivisions }
  }
})
</script>
