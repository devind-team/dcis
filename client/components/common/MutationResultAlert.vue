<template lang="pug">
div
  template(v-if="error")
    v-alert(v-if="error.value.type === 'BusinessLogicError'" type="error" color="orange")
      | {{ $t('common.mutationResultAlert.mutationBusinessLogicError', { error: error.value.message }) }}
    v-alert(v-else-if="error.value.type === 'GraphQLError'" type="error")
      | {{ $t('common.mutationResultAlert.mutationGraphQLError', { error: error.value.message }) }}
    v-alert(v-else type="error") {{ $t('common.mutationResultAlert.mutationNetworkError', { error: error.value.message }) }}
  error-validate-dialog(v-else-if="tableErrors" v-slot="{ on: onDialog }" v-bind="tableErrors")
    v-tooltip(bottom)
      template(#activator="{ on: onTooltip }")
        v-alert(v-on="{ ...onDialog, ...onTooltip }" type="error" style="cursor: pointer")
          | {{ $t('common.mutationResultAlert.tableMutationErrors') }}
      span {{ $t('common.mutationResultAlert.showDetails') }}
  v-alert(v-else-if="success" type="success") {{ successMessage }}
</template>

<script lang="ts">
import { ApolloError } from 'apollo-client'
import { defineComponent, ref } from '#app'
import { ErrorType, WithTimer } from '~/types/devind'
import { ErrorFieldType, TableType } from '~/types/graphql'
import ErrorValidateDialog from '~/components/common/dialogs/ErrorValidateDialog.vue'

export type TableErrors = {
  table: TableType,
  errors: ErrorFieldType[]
}

export default defineComponent({
  components: { ErrorValidateDialog },
  props: {
    hideTimeout: { type: Number, default: 20000 },
    successMessage: {
      type: String,
      default (): string {
        return this.$t('common.mutationResultAlert.mutationSuccess') as string
      }
    }
  },
  setup (props) {
    const success = ref<WithTimer<boolean> | null>(null)
    const error = ref<WithTimer<{ message: string, type: ErrorType }>>(null)
    const tableErrors = ref<TableErrors | null>(null)

    const setApolloError = (error: ApolloError): void => {
      if (error.networkError) {
        setError(error.networkError.message, 'NetworkError')
      } else {
        setError(error.graphQLErrors[0].message, 'GraphQLError')
      }
    }

    const clearTimer = (): void => {
      if (error.value && error.value.timerId) {
        clearTimeout(error.value.timerId)
      }
      if (success.value && success.value.timerId) {
        clearTimeout(success.value.timerId)
      }
    }

    const setError = (message: string, type: ErrorType): void => {
      clearTimer()
      success.value = null
      tableErrors.value = null
      error.value = {
        value: { message, type },
        timerId: Number.isFinite(props.hideTimeout)
          ? setTimeout(() => { error.value = null }, props.hideTimeout)
          : null
      }
    }

    const setSuccess = (): void => {
      clearTimer()
      error.value = null
      tableErrors.value = null
      success.value = {
        value: true,
        timerId: Number.isFinite(props.hideTimeout)
          ? setTimeout(() => { success.value = null }, props.hideTimeout)
          : null
      }
    }

    const setTableErrors = (te: TableErrors): void => {
      clearTimer()
      error.value = null
      success.value = null
      tableErrors.value = te
    }

    const clear = (): void => {
      clearTimer()
      error.value = null
      success.value = null
      tableErrors.value = null
    }

    return {
      success,
      error,
      tableErrors,
      setApolloError,
      setError,
      setSuccess,
      setTableErrors,
      clear
    }
  }
})
</script>
