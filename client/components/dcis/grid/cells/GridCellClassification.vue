<template lang="pug">
v-dialog(v-model="active" width="600px" scrollable)
  template(#activator="{ on }")
    div(v-on="on") {{ value }}
  v-card(:loading="loading")
    v-card-title {{ $t('dcis.grid.changeValue') }}
      v-spacer
      v-btn(@click="close" icon)
        v-icon mdi-close
    v-card-text
      v-text-field(
        v-model="search"
        :label="$t('search')"
        :hint="$t('shownOf', { count, totalCount })"
        autofocus
        persistent-hint
        flat
        clearable
      )
    v-divider
    template(v-if="!loading && classifications.length === 0")
      v-card-text(style="height: 248px;")
        v-textarea(v-model="name" label="Комментарий" success)
      v-card-actions
        v-spacer
        v-btn(@click="mutate({ code: search, name })" color="primary") Добавить
    v-card-text(v-else style="height: 300px;")
      v-list
        v-list-item(v-for="classification in classifications" :key="classification.id" @click="setValue(classification)")
          v-list-item-content
            v-list-item-title {{ classification.code }}
            .caption {{ classification.name }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { useMutation } from '@vue/apollo-composable'
import { defineComponent, ref } from '#app'
import { useDebounceSearch, useQueryRelay, useCursorPagination } from '~/composables'
import {
  AddBudgetClassificationMutationPayload,
  CreateBudgetClassificationInput,
  BudgetClassificationsQuery,
  BudgetClassificationsQueryVariables,
  BudgetClassificationType
} from '~/types/graphql'
import activeBudgetClassificationsQuery from '~/gql/dcis/queries/active_budget_classifications.graphql'
import addBudgetClassificationMutation from '~/gql/dcis/mutations/cell/add_budget_classification.graphql'

export default defineComponent({
  props: {
    value: { type: String, default: null }
  },
  setup (props, { emit }) {
    const { search, debounceSearch } = useDebounceSearch({ defaultValue: props.value })
    const active = ref<boolean>(true)
    const name = ref<string>('')

    const {
      data: classifications,
      loading,
      pagination: { count, totalCount },
      addUpdate
    } = useQueryRelay<
      BudgetClassificationsQuery,
      BudgetClassificationsQueryVariables,
      BudgetClassificationType
    >({
      document: activeBudgetClassificationsQuery,
      variables: () => ({ code: debounceSearch.value })
    }, {
      pagination: useCursorPagination({ pageSize: 20 })
    })

    const { mutate } = useMutation<
      AddBudgetClassificationMutationPayload,
      CreateBudgetClassificationInput
    >(addBudgetClassificationMutation, {
      update: (cache: DataProxy | any, result: { data: AddBudgetClassificationMutationPayload }) =>
        addUpdate(cache, result, 'budgetClassification')
    })

    const setValue = (classification: BudgetClassificationType) => {
      active.value = false
      emit('set-value', classification.code)
    }

    const close = () => {
      active.value = false
      emit('cancel')
    }

    return { active, name, search, loading, classifications, count, totalCount, mutate, setValue, close }
  }
})
</script>
