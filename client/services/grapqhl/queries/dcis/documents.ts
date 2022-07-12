import { Ref, unref } from '#app'
import { DocumentsQuery, DocumentsQueryVariables, DocumentType } from '~/types/graphql'
import documentsQuery from '~/gql/dcis/queries/documents.graphql'

export const useDocumentsQuery = (periodId: Ref<string> | string) => {
  return useQueryRelay<DocumentsQuery, DocumentsQueryVariables, DocumentType>({
    document: documentsQuery,
    variables: () => ({ periodId: unref(periodId) })
  })
}
