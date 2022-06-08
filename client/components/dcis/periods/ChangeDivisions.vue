<template lang="pug">
  mutation-modal-form(
    :header="String($t('dcis.periods.divisions.formHeader'))"
    :button-text="String($t('dcis.periods.divisions.buttonText'))"
    :mutation="changeDivisions"
    :update="changeDivisionsUpdate"
    :variables="{ periodId: period.id, divisionIds: divisionsListId }"
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
        :headers="headers"
        :items="[]"
        :loading="loading"
        :search="search"
        item-key="id"
        disable-pagination
        show-select
        hide-default-footer
      )
        template(#item.createdAt="{ item }") {{ dateTimeHM(item.createdAt) }}
</template>

<script lang="ts">
import { ref, defineComponent, PropType } from '#app'
import { DataTableHeader } from 'vuetify'
import { DataProxy } from 'apollo-cache'
import { ChangeDivisionsMutationPayload, PeriodType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { useDebounceSearch, useFilters, useI18n } from '~/composables'
import changeDivisions from '~/gql/dcis/mutations/project/change_divisions.graphql'

export type ChangeDivisionsMutationResult = { data: { changeDivisions: ChangeDivisionsMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: ChangeDivisionsMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    loading: { type: Boolean as PropType<boolean>, default: false },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const { t } = useI18n()
    const { dateTimeHM } = useFilters()
    const { search } = useDebounceSearch()
    const divisionsListId = ref<string[]>([])

    const headers: DataTableHeader[] = [
      { text: t('dcis.periods.divisions.name') as string, value: 'name' },
      { text: t('dcis.periods.divisions.createdAt') as string, value: 'createdAt', width: 150 }
    ]
    const changeDivisionsUpdate = (cache: DataProxy, result: ChangeDivisionsMutationResult) => {
      const { success } = result.data.changeDivisions
      if (success) {
        props.update(cache, result)
      }
    }
    return { headers, changeDivisions, divisionsListId, search, dateTimeHM, changeDivisionsUpdate }
  }
})
</script>
