import { Ref, unref } from '#app'
import { useCommonQuery } from '~/composables'
import { PeriodQuery, PeriodQueryVariables } from '~/types/graphql'
import periodQuery from '~/gql/dcis/queries/period.graphql'

export const usePeriodQuery = (periodId: Ref<string> | string) => useCommonQuery<PeriodQuery, PeriodQueryVariables>({
  document: periodQuery,
  variables: { periodId: unref(periodId) }
})
