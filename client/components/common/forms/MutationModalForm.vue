<template lang="pug">
v-dialog(
  v-model="active"
  :width="width"
  :fullscreen="fullscreen"
  :persistent="persistent"
  scrollable
  @click:outside="$emit('click:outside')"
)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs" :close="close")
  mutation-form(
    ref="mutationForm"
    v-bind="$attrs"
    :mutation-name="mutationName"
    :errors-in-alert="errorsInAlert"
    :show-success="showSuccess"
    :header="header"
    :subheader="subheader"
    :button-text="buttonText"
    :i18n-path="i18nPath"
    :hide-alert-timeout="hideAlertTimeout"
    :hide-actions="hideActions"
    :success-message="successMessage"
    :table-errors-mode="tableErrorsMode"
    :table-errors-message="tableErrorsMessage"
    :table-errors-title="tableErrorsTitle"
    :show-table-errors-search="showTableErrorsSearch"
    v-on="mutationListeners"
  )
    template(#header)
      slot(name="header" :header="header")
        span {{ header }}
      v-spacer
      v-btn(v-if="canMinimize" @click="active = false" icon)
        v-icon mdi-minus
      v-btn(@click="close" icon)
        v-icon mdi-close
    template(#subheader)
      slot(name="subheader" :subheader="subheader") {{ subheader }}
    template(#form)
      slot(name="form")
    template(#actions="{ invalid, loading, buttonText, setFormErrors, setError, setSuccess }")
      slot(
        name="actions"
        :button-text="buttonText"
        :invalid="invalid"
        :loading="loading"
        :set-form-errors="setFormErrors"
        :set-error="setError"
        :set-success="setSuccess"
      )
        v-spacer
        v-btn(:disabled="invalid" :loading="loading" type="submit" color="primary") {{ buttonText }}
</template>

<script lang="ts">
import { VueConstructor } from 'vue'
import { watchOnce } from '@vueuse/core'
import { computed, defineComponent, getCurrentInstance, PropType, ref, watch } from '#app'
import { ErrorValidateDialogMode } from '~/components/common/dialogs/ErrorValidateDialog.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm },
  inheritAttrs: false,
  props: {
    mutationName: { type: [String, Array], required: true },
    successClose: { type: Boolean, default: true },
    errorsInAlert: { type: Boolean, default: false },
    showSuccess: { type: Boolean, default: true },
    fullscreen: { type: Boolean, default: false },
    persistent: { type: Boolean, default: false },
    canMinimize: { type: Boolean, default: false },
    header: { type: String, default: '' },
    subheader: { type: String, default: '' },
    buttonText: { type: String, default: '' },
    i18nPath: { type: String, default: '' },
    width: { type: [String, Number], default: 600 },
    hideAlertTimeout: { type: Number, default: 5000 },
    hideActions: { type: Boolean, default: false },
    successMessage: { type: String, default: '' },
    tableErrorsMode: { type: Number as PropType<ErrorValidateDialogMode>, default: ErrorValidateDialogMode.TOOLTIP },
    tableErrorsMessage: { type: String, default: null },
    tableErrorsTitle: { type: String, default: null },
    showTableErrorsSearch: { type: Boolean, default: true }
  },
  setup (props, { emit }) {
    const instance = getCurrentInstance()
    const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>

    const mutationForm = ref<InstanceType<typeof MutationForm>>(null)
    const active = ref<boolean>(false)

    const mutationListeners = computed(() => (
      Object.assign({}, vm.$listeners, {
        done (result: any) {
          const mutationNames = (
            Array.isArray(props.mutationName)
              ? props.mutationName
              : [props.mutationName]
          ) as string[]
          const success = mutationNames.every((mutationName: string) => result.data[mutationName].success && !result.data[mutationName].errors.length)
          if (success && props.successClose) {
            close()
          }
          emit('done', result)
        }
      })
    ))

    watch(() => active.value, (newValue) => {
      emit('active-changed', newValue)
    })
    watchOnce(() => active.value, (newValue) => {
      if (newValue) {
        emit('first-activated')
      }
    })

    const close = () => {
      active.value = false
      mutationForm.value.clear()
      emit('close')
    }

    return { active, mutationForm, mutationListeners, close }
  }
})
</script>
