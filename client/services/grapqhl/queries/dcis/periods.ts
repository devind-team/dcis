import { Ref, unref } from '#app'
import { useCommonQuery } from '~/composables'
import { PeriodQuery, PeriodQueryVariables, PeriodsQuery, PeriodsQueryVariables } from '~/types/graphql'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'
import periodQuery from '~/gql/dcis/queries/period.graphql'

export const usePeriodsQuery = (projectId: Ref<string> | string) => {
  return useCommonQuery<PeriodsQuery, PeriodsQueryVariables>({
    document: periodsQuery,
    variables: { projectId: unref(projectId) }
  })
}

export const usePeriodQuery = (periodId: Ref<string> | string) => {
  return useCommonQuery<PeriodQuery, PeriodQueryVariables>({
    document: periodQuery,
    variables: { periodId: unref(periodId) }
  })
}
