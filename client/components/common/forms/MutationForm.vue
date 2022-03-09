<template lang="pug">
  apollo-mutation(
    v-slot="{ mutate, loading }"
    v-bind="$attrs"
    v-on="mutationListeners"
    tag
  )
    validation-observer(v-slot="{ handleSubmit, invalid }" ref="validationObserver" slim)
      form(@submit.prevent="handleSubmit(mutate)")
        v-card
          v-card-title
            slot(name="header" :header="header")
              span {{ header }}
          v-card-subtitle
            slot(name="subheader" :subheader="subheader")
              span {{ subheader }}
          v-card-text
            mutation-result-alert(
              ref="mutationResultAlert"
              :hide-timeout="hideAlertTimeout"
              :success-message="successMessage"
            )
            slot(name="form")
          v-card-actions
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
import Vue from 'vue'
import { ApolloError } from 'apollo-client'
import { ErrorFieldType } from '~/types/graphql'
import { ErrorType } from '~/types/devind'
import MutationResultAlert, { TableErrors } from '~/components/common/MutationResultAlert.vue'

export default Vue.extend<any, any, any, any>({
  components: { MutationResultAlert },
  inheritAttrs: false,
  props: {
    mutationName: { type: String, required: true },
    errorsInAlert: { type: Boolean, default: false },
    header: { type: String, default: '' },
    subheader: { type: String, default: '' },
    buttonText: { type: String, default: '' },
    i18nPath: { type: String, default: '' },
    hideAlertTimeout: { type: Number, default: 20000 },
    successMessage: { type: String, default: '' }
  },
  computed: {
    mutationListeners () {
      const vm = this
      return Object.assign({}, this.$listeners, {
        error (error: ApolloError): void {
          vm.setApolloError(error)
          vm.$emit('error', error)
        },
        done (result: any): void {
          vm.mutationDone(result)
          vm.$emit('done', result)
        }
      })
    }
  },
  methods: {
    /**
     * Установка ошибки Apollo
     * @param error
     */
    setApolloError (error: ApolloError): void {
      this.$refs.mutationResultAlert.setApolloError(error)
    },
    /**
     * Установка ошибки
     * @param message
     * @param type
     */
    setError (message: string, type: ErrorType): void {
      this.$refs.mutationResultAlert.setError(message, type)
    },
    /**
     * Установка успеха
     */
    setSuccess (): void {
      this.$refs.mutationResultAlert.setSuccess()
    },
    /**
     * Установка таблицы ошибок
     */
    setTableErrors (tableErrors: TableErrors): void {
      this.$refs.mutationResultAlert.setTableErrors(tableErrors)
    },
    /**
     * Установка ошибок после мутации
     * @param errors
     * @param showInAlert
     */
    setFormErrors (errors: ErrorFieldType[], showInAlert: boolean = false): void {
      if (showInAlert) {
        const errorString: string = errors.reduce((a: string, c: ErrorFieldType) =>
          a.concat(c.messages.join(', ')), '')
        this.setError(errorString, 'BusinessLogicError')
      } else {
        this.$refs.validationObserver.setErrors(errors.reduce(
          (a: { [key: string]: string[] }, c: ErrorFieldType) => {
            return {
              ...a,
              [this.$t(`${this.i18nPath}.${this.$snakeToCamel(c.field)}`) as string]: c.messages
            }
          }, {}))
      }
    },
    /**
     * Обработка окончания выполнения мутации
     * @param result
     */
    mutationDone (result: any): void {
      const { success, errors, table } = result.data[this.mutationName]
      if (success) {
        this.setSuccess()
      } else {
        const tableErrors = table ? { table, errors } : null
        if (tableErrors) {
          this.setTableErrors(tableErrors)
        } else {
          this.setFormErrors(errors, this.errorsInAlert)
        }
      }
    },
    /**
     * Очистка валидатора и результата мутации
     */
    clear (): void {
      this.$refs.mutationResultAlert.clear()
      this.$nextTick(() => { this.$refs.validationObserver.reset() })
    }
  }
})
</script>
