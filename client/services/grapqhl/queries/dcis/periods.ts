import { useCommonQuery } from '~/composables'
import { PeriodsQuery, PeriodsQueryVariables } from '~/types/graphql'
import periodsQuery from '~/gql/dcis/queries/periods.graphql'

export const usePeriodsQuery = (projectId: string) => {
  return useCommonQuery<PeriodsQuery, PeriodsQueryVariables>({
    document: periodsQuery,
    variables: { projectId }
  })
}
