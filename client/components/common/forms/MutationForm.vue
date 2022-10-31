<template lang="pug">
apollo-mutation(
  v-slot="{ mutate, loading }"
  v-bind="$attrs"
  v-on="mutationListeners"
  tag
)
  validation-observer(v-slot="{ handleSubmit, invalid }" ref="validationObserver" slim)
    form(@submit.prevent="handleSubmit(mutate)")
      v-card(:flat="flat")
        v-card-title(v-if="header")
          slot(name="header" :header="header") {{ header }}
        v-card-subtitle(v-if="subheader")
          slot(name="subheader" :subheader="subheader")
            span {{ subheader }}
        v-card-text
          mutation-result-alert(
            ref="mutationResultAlert"
            :hide-timeout="hideAlertTimeout"
            :success-message="successMessage"
          )
          slot(name="form")
        v-card-actions(v-if="!hideActions")
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
import { camelCase } from 'scule'
import { VueConstructor } from 'vue'
import { ApolloError } from 'apollo-client'
import { ValidationObserver } from 'vee-validate'
import { defineComponent, computed, getCurrentInstance, ref, nextTick } from '#app'
import { useI18n } from '~/composables'
import { ErrorFieldType } from '~/types/graphql'
import { ErrorType } from '~/types/devind'
import MutationResultAlert, { TableErrors } from '~/components/common/MutationResultAlert.vue'

type MutationResultAlertType = InstanceType<typeof MutationResultAlert> | null
type ValidationObserverType = InstanceType<typeof ValidationObserver> | null

export default defineComponent({
  components: { MutationResultAlert },
  inheritAttrs: false,
  props: {
    mutationName: { type: [String, Array], required: true },
    errorsInAlert: { type: Boolean, default: false },
    showSuccess: { type: Boolean, default: true },
    successMessage: { type: String, default: '' },
    header: { type: String, default: '' },
    subheader: { type: String, default: '' },
    buttonText: { type: String, default: '' },
    i18nPath: { type: String, default: '' },
    hideAlertTimeout: { type: Number, default: 20000 },
    flat: { type: Boolean, default: false },
    hideActions: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const instance = getCurrentInstance()
    const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>
    const validationObserver = ref<ValidationObserverType>(null)
    // @ts-ignore: TS2322
    const mutationResultAlert = ref<MutationResultAlertType>(null)

    const setApolloError = (error: ApolloError): void => {
      mutationResultAlert.value.setApolloError(error)
    }

    const setError = (message: string, type: ErrorType): void => {
      mutationResultAlert.value.setError(message, type)
    }

    const setSuccess = (): void => {
      mutationResultAlert.value.setSuccess()
    }

    const setTableErrors = (tableErrors: TableErrors): void => {
      mutationResultAlert.value.setTableErrors(tableErrors)
    }

    const setFormErrors = (errors: ErrorFieldType[], showInAlert: boolean = false): void => {
      const allFields = errors.map((e: ErrorFieldType) => e.field).includes('__all__')
      if (allFields || showInAlert) {
        const errorString: string = errors.reduce((a: string, c: ErrorFieldType) =>
          a ? `${a}, ${c.messages.join(', ')}` : c.messages.join(', '), '')
        setError(errorString, 'BusinessLogicError')
      } else {
        validationObserver.value.setErrors(errors.reduce(
          (a: { [key: string]: string[] }, c: ErrorFieldType) => {
            return {
              ...a,
              [t(`${props.i18nPath}.${camelCase(c.field)}`) as string]: c.messages
            }
          }, {}))
      }
    }

    const mutationDone = (result: any): void => {
      const mutationNames = (Array.isArray(props.mutationName) ? props.mutationName : [props.mutationName]) as string[]
      const mutationsErrors: ErrorFieldType[] = []
      for (const mutationName of mutationNames) {
        const { success, errors, table } = result.data[mutationName]
        if (!success) {
          const tableErrors = table ? { table, errors } : null
          if (tableErrors) {
            setTableErrors(tableErrors)
            return
          } else {
            mutationsErrors.push(...errors)
          }
        }
      }
      if (mutationsErrors.length) {
        setFormErrors(mutationsErrors, props.errorsInAlert)
      } else if (props.showSuccess) {
        setSuccess()
      }
    }

    const mutationListeners = computed(() => (Object.assign({}, vm.$listeners, {
      error (error: ApolloError): void {
        setApolloError(error)
        emit('error', error)
      },
      done (result: any): void {
        mutationDone(result)
        emit('done', result)
      }
    })))

    /**
     * Очистка валидатора и результата мутации
     */
    const clear = (): void => {
      mutationResultAlert.value.clear()
      nextTick(() => {
        validationObserver.value.reset()
      })
    }

    return { mutationListeners, setFormErrors, setError, setSuccess, clear, validationObserver, mutationResultAlert }
  }
})
</script>
