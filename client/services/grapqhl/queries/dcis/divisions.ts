import { useCommonQuery } from '~/composables'
import { UserDivisionsQuery, UserDivisionsQueryVariables } from '~/types/graphql'
import userDivisionsQuery from '~/gql/dcis/queries/user_divisions.graphql'

export const useUserDivisions = (userId: string | undefined = undefined, projectId: string | undefined = undefined) => {
  return useCommonQuery<UserDivisionsQuery, UserDivisionsQueryVariables>({
    document: userDivisionsQuery,
    variables: { userId, projectId }
  })
}
