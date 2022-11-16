<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.limitations.changeLimitation.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.limitations.changeLimitation.header'))"
  :mutation="changeLimitationMutation"
  :variables="variables"
  mutation-name="changeLimitation"
  i18n-path="dcis.periods.limitations.changeLimitation"
  @close="close"
)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeLimitation.formula'))"
      rules="required"
    )
      v-text-field(
        v-model="formula"
        :label="$t('dcis.periods.limitations.changeLimitation.formula')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeLimitation.errorMessage'))"
      rules="required|min:3"
    )
      v-text-field(
        v-model="errorMessage"
        :label="$t('dcis.periods.limitations.changeLimitation.errorMessage')"
        :error-messages="errors"
        :success="valid"
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeLimitation.sheet'))"
      rules="required"
    )
      v-select(
        v-model="sheet"
        :items="period.sheets"
        :label="$t('dcis.periods.limitations.changeLimitation.sheet')"
        :error-messages="errors"
        :success="valid"
        item-text="name"
        return-object
      )
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { PeriodType, BaseSheetType, LimitationType, ChangeLimitationMutationVariables } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import changeLimitationMutation from '~/gql/dcis/mutations/limitation/change_limitation.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    limitation: { type: Object as PropType<LimitationType>, required: true }
  },
  setup (props) {
    const formula = ref<string>(props.limitation.formula)
    const errorMessage = ref<string>(props.limitation.errorMessage)
    const sheet = ref<BaseSheetType>(props.limitation.sheet)

    const variables = computed<ChangeLimitationMutationVariables>(() => ({
      limitationId: props.limitation.id,
      formula: formula.value,
      errorMessage: errorMessage.value,
      sheetId: sheet.value.id
    }))

    const close = () => {
      formula.value = props.limitation.formula
      errorMessage.value = props.limitation.errorMessage
      sheet.value = props.limitation.sheet
    }

    return {
      changeLimitationMutation,
      formula,
      errorMessage,
      sheet,
      variables,
      close
    }
  }
})
</script>
