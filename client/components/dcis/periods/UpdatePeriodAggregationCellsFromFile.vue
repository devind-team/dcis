<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.buttonText'))"
  :mutation="updateAggregationFromFileMutation"
  :variables="variables"
  :update="update"
  mutation-name="updateAggregationsFromFile"
  i18n-path="dcis.periods.aggregationCells.changeMenu.updateAggregationFile"
  @close="close"
)
  template(#activator="{ on, attrs}")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.aggregationsFile'))"
      rules="required"
    )
      v-file-input(
        v-model="aggregationsFile"
        :label="$t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.aggregationsFile')"
        :error-messages="errors"
        :success="valid"
        accept=".json"
     )
        template(#append-outer)
          v-tooltip(bottom)
            template(#activator="{ on, attrs }")
              v-btn(v-bind="attrs" v-on="on" href="/templates/Агрегация.json" small icon download)
                v-icon mdi-file-download
            span {{ $t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.downloadTemplate') }}
</template>

<script lang="ts">

import { defineComponent, PropType, computed } from '#app'
import { ResetUpdateType } from '~/composables'
import { PeriodType, UpdateAggregationsFromFileMutationVariables } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import updateAggregationFromFileMutation from '~/gql/dcis/mutations/aggregation/update_aggregations_from_file.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<ResetUpdateType>, required: true }
  },
  setup (props) {
    const aggregationsFile = ref<File | null>(null)

    const variables = computed<UpdateAggregationsFromFileMutationVariables>(() => ({
      periodId: props.period.id,
      aggregationsFile: aggregationsFile.value
    }))

    const close = () => {
      aggregationsFile.value = null
    }

    return {
      updateAggregationFromFileMutation,
      aggregationsFile,
      variables,
      close
    }
  }
})
</script>
