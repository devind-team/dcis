<template lang="pug">
mutation-modal-form(
  :header="header"
  :subheader="period.name"
  :button-text="buttonText"
  :mutation="addPeriodDivisionsFromFileMutation"
  :variables="{ periodId: period.id, file }"
  :update="update"
  width="40vw"
  mutation-name="addDivisionsFromFile"
  i18n-path="dcis.periods.addDivisions"
  errors-in-alert
  @close="$emit('close')"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(v-slot="{ error, valid }" :name="String($t('dcis.periods.file'))" rules="required")
      v-file-input(
        v-model="file"
        :label="String($t('dcis.periods.addDivisions.file'))"
        placeholder="Выберете файл"
        hint="Файл в формате xlsx"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        persistent-hint clearable)
</template>

<script lang="ts">

import { defineComponent, PropType, ref } from '#app'
import { DataProxy } from 'apollo-cache'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { AddDivisionsFromFileMutationPayload, PeriodType } from '~/types/graphql'
import addPeriodDivisionsFromFileMutation from '~/gql/dcis/mutations/period/add_divisions_from_file.graphql'

export type AddDivisionsFromFileMutationResult = { data: { addDivisionsFromFile: AddDivisionsFromFileMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddDivisionsFromFileMutationResult) => void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    header: { type: String, required: true },
    buttonText: { type: String, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup () {
    const file = ref<File | null>(null)
    return { addPeriodDivisionsFromFileMutation, file }
  }
})
</script>
