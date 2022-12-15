import { QueryRelayResult, useCursorPagination, useQueryRelay } from '~/composables'
import projectsQuery from '~/gql/dcis/queries/projects.graphql'
import { ProjectsQuery, ProjectsQueryVariables, ProjectType } from '~/types/graphql'

export const useProjects = (): QueryRelayResult<ProjectsQuery, ProjectsQueryVariables, ProjectType> => {
  return useQueryRelay<ProjectsQuery, ProjectsQueryVariables, ProjectType>({
    document: projectsQuery
  }, {
    isScrollDown: true,
    pagination: useCursorPagination()
  })
}
