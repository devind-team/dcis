<template lang="pug">
  v-menu(v-model="active" :close-on-content-click="false" bottom)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    .v-dialog--scrollable
      v-card(:loading="loading" style="width: 400px;")
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
        v-card-text(style="height: 200px;")
          v-list
            v-list-item(v-for="classification in classifications" :key="classification.id" @click="setValue(classification)")
              v-tooltip(bottom)
                template(#activator="{ on }")
                  v-list-item-content(v-on="on")
                    v-list-item-title {{ classification.code }}
                span {{ classification.name }}
        v-divider
        v-card-actions
          v-btn(@click="close") {{ $t('cancel') }}
          v-spacer
</template>

<script lang="ts">
import {
  BudgetClassificationsQuery,
  BudgetClassificationsQueryVariables,
  BudgetClassificationType
} from '~/types/graphql'
import budgetClassificationsQuery from '~/gql/dcis/queries/budget_classifications.graphql'

export default defineComponent({
  props: {
    value: { type: String, required: true }
  },
  setup (props, { emit }) {
    const { search, debounceSearch } = useDebounceSearch()
    search.value = props.value
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
      document: budgetClassificationsQuery,
      variables: () => ({ code: debounceSearch.value })
    }, {
      pagination: useCursorPagination({ pageSize: 20 })
    })

    const setValue = (classification: BudgetClassificationType) => {
      console.log(classification)
    }

    const close = () => {
      active.value = false
      emit('cancel')
    }

    return { active, search, loading, classifications, count, totalCount, setValue, close }
  }
})
</script>
