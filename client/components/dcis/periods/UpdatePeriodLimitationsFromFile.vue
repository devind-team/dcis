<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.buttonText'))"
  :mutation="updateLimitationsFromFileMutation"
  :variables="variables"
  :update="update"
  mutation-name="updateLimitationsFromFile"
  i18n-path="dcis.periods.limitations.changeMenu.updateLimitationFromFile"
  @close="close"
)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.limitationsFile'))"
      rules="required"
    )
      v-file-input(
        v-model="limitationsFile"
        :label="$t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.limitationsFile')"
        :error-messages="errors"
        :success="valid"
        accept=".json"
      )
        template(#append-outer)
          v-tooltip(bottom)
            template(#activator="{ on, attrs }")
              v-btn(v-bind="attrs" v-on="on" href="/templates/Ограничения.json" small icon download)
                v-icon mdi-file-download
            span {{ $t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.downloadTemplate') }}
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from '#app'
import { ResetUpdateType } from '~/composables'
import { PeriodType, UpdateLimitationsFromFileMutationVariables } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import updateLimitationsFromFileMutation from '~/gql/dcis/mutations/limitation/update_limitations_from_file.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<ResetUpdateType>, required: true }
  },
  setup (props) {
    const limitationsFile = ref<File | null>(null)

    const variables = computed<UpdateLimitationsFromFileMutationVariables>(() => ({
      periodId: props.period.id,
      limitationsFile: limitationsFile.value
    }))

    const close = () => {
      limitationsFile.value = null
    }

    return { updateLimitationsFromFileMutation, limitationsFile, variables, close }
  }
})
</script>
