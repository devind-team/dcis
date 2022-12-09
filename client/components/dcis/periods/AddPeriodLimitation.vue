<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.limitations.changeMenu.addLimitation.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.limitations.changeMenu.addLimitation.buttonText'))"
  :mutation="addLimitationMutation"
  :variables="variables"
  :update="(cache, result) => update(cache, result, 'limitation', false)",
  mutation-name="addLimitation"
  i18n-path="dcis.periods.limitations.changeMenu.addLimitation"
  @close="close"
)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeMenu.addLimitation.formula'))"
      rules="required"
    )
      v-text-field(
        v-model="formula"
        :label="$t('dcis.periods.limitations.changeMenu.addLimitation.formula')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeMenu.addLimitation.errorMessage'))"
      rules="required|min:3"
    )
      v-text-field(
        v-model="errorMessage"
        :label="$t('dcis.periods.limitations.changeMenu.addLimitation.errorMessage')"
        :error-messages="errors"
        :success="valid"
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.limitations.changeMenu.addLimitation.sheet'))"
      rules="required"
    )
      v-select(
        v-model="sheet"
        :items="period.sheets"
        :label="$t('dcis.periods.limitations.changeMenu.addLimitation.sheet')"
        :error-messages="errors"
        :success="valid"
        item-text="name"
        return-object
      )
</template>

<script lang="ts">
import { defineComponent, ref, computed, PropType } from '#app'
import { AddUpdateType } from '~/composables'
import { PeriodType, BaseSheetType, AddLimitationMutationVariables } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import addLimitationMutation from '~/gql/dcis/mutations/limitation/add_limitation.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<AddUpdateType>, required: true }
  },
  setup () {
    const formula = ref<string>('')
    const errorMessage = ref<string>('')
    const sheet = ref<BaseSheetType | null>(null)

    const variables = computed<AddLimitationMutationVariables>(() => ({
      formula: formula.value,
      errorMessage: errorMessage.value,
      sheetId: sheet.value ? sheet.value.id : ''
    }))

    const close = () => {
      formula.value = ''
      errorMessage.value = ''
      sheet.value = null
    }

    return {
      addLimitationMutation,
      formula,
      errorMessage,
      sheet,
      variables,
      close
    }
  }
})
</script>
