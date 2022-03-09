<template lang="pug">
  div
    template(v-if="error")
      v-alert(v-if="error.value.type === 'BusinessLogicError'" type="error" color="orange")
        | {{ t('mutationBusinessLogicError', { error: error.value.message }) }}
      v-alert(v-else-if="error.value.type === 'GraphQLError'" type="error")
        | {{ t('mutationGraphQLError', { error: error.value.message }) }}
      v-alert(v-else type="error") {{ t('mutationNetworkError', { error: error.value.message }) }}
    error-validate-dialog(v-else-if="tableErrors" v-slot="{ on: onDialog }" v-bind="tableErrors")
      v-tooltip(bottom)
        template(#activator="{ on: onTooltip }")
          v-alert(v-on="{ ...onDialog, ...onTooltip }" type="error" style="cursor: pointer")
            | {{ t('tableMutationErrors') }}
        span {{ t('showDetails') }}
    v-alert(v-else-if="success" type="success") {{ successMessage ? successMessage : t('mutationSuccess') }}
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { ApolloError } from 'apollo-client'
import { ErrorType, WithTimer } from '~/types/devind'
import { ErrorFieldType, TableType } from '~/types/graphql'
import ErrorValidateDialog from '~/components/common/dialogs/ErrorValidateDialog.vue'

export type TableErrors = {
  table: TableType,
  errors: ErrorFieldType[]
}

@Component<MutationResultAlert>({
  components: { ErrorValidateDialog }
})
export default class MutationResultAlert extends Vue {
  @Prop({ type: Number, default: 20000 }) readonly hideTimeout!: number
  @Prop({ type: String }) readonly successMessage?: string

  error: WithTimer<{ message: string, type: ErrorType }> | null = null
  success: WithTimer<boolean> | null = null
  tableErrors: TableErrors | null = null

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values?: any): string {
    return this.$t(`common.mutationResultAlert.${path}`, values) as string
  }

  /**
   * Установка ошибки Apollo
   * @param error
   */
  setApolloError (error: ApolloError): void {
    if (error.networkError) {
      this.setError(error.networkError.message, 'NetworkError')
    } else {
      this.setError(error.graphQLErrors[0].message, 'GraphQLError')
    }
  }

  /**
   * Установка ошибки
   * @param message
   * @param type
   */
  setError (message: string, type: ErrorType): void {
    if (this.error && this.error.timerId) {
      clearTimeout(this.error!.timerId)
    }
    if (this.success && this.success.timerId) {
      clearTimeout(this.success!.timerId)
    }
    this.success = null
    this.tableErrors = null
    this.error = {
      value: { message, type },
      timerId: Number.isFinite(this.hideTimeout)
        ? setTimeout(() => { this.error = null }, this.hideTimeout)
        : null
    }
  }

  /**
   * Установка успеха
   */
  setSuccess (): void {
    if (this.error && this.error.timerId) {
      clearTimeout(this.error!.timerId)
    }
    if (this.success && this.success.timerId) {
      clearTimeout(this.success!.timerId)
    }
    this.error = null
    this.tableErrors = null
    this.success = {
      value: true,
      timerId: Number.isFinite(this.hideTimeout)
        ? setTimeout(() => { this.success = null }, this.hideTimeout)
        : null
    }
  }

  /**
   * Установка таблицы ошибок
   */
  setTableErrors (tableErrors: TableErrors): void {
    if (this.error && this.error.timerId) {
      clearTimeout(this.error!.timerId)
    }
    if (this.success && this.success.timerId) {
      clearTimeout(this.success!.timerId)
    }
    this.error = null
    this.success = null
    this.tableErrors = tableErrors
  }

  /**
   * Очистка сообщений
   */
  clear () {
    if (this.error && this.error.timerId) {
      clearTimeout(this.error!.timerId)
    }
    if (this.success && this.success.timerId) {
      clearTimeout(this.success!.timerId)
    }
    this.error = null
    this.success = null
    this.tableErrors = null
  }
}
</script>
