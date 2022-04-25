<template lang="pug">
  v-dialog(v-model="active" width="600px" scrollable)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    v-card(:loading="loading")
      v-card-title Изменение значения
        v-spacer
        v-btn(@click="close" icon)
          v-icon mdi-close
      v-card-text
        v-text-field(
          v-model="search"
          :label="$t('search')"
          :hint="$t('shownOf', { count, totalCount })"
          persistent-hint
          flat
          clearable
        )
      v-divider
      v-card-text(style="height: 300px;")
        v-list
          v-list-item(v-for="classification in classifications" :key="classification.id" @click="setValue(classification)")
            v-list-item-content(v-on="on")
              v-list-item-title {{ classification.code }}
              .caption {{ classification.name }}
</template>

<script lang="ts">
import {
  BudgetClassificationsQuery,
  BudgetClassificationsQueryVariables,
  BudgetClassificationType
} from '~/types/graphql'
import activeBudgetClassificationsQuery from '~/gql/dcis/queries/active_budget_classifications.graphql'

export default defineComponent({
  props: {
    value: { type: String, required: true }
  },
  setup (props, { emit }) {
    const { search, debounceSearch } = useDebounceSearch()
    search.value = debounceSearch.value = props.value
    const active = ref<boolean>(true)

    const {
      data: classifications,
      loading,
      pagination: { count, totalCount }
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

    const setValue = (classification: BudgetClassificationType) => {
      active.value = false
      emit('set-value', classification.code)
    }

    const close = () => {
      active.value = false
      emit('cancel')
    }

    return { active, search, loading, classifications, count, totalCount, setValue, close }
  }
})
</script>
