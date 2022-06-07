import { useMutation } from '@vue/apollo-composable'
import { MutationUpdaterFn } from '@apollo/client'
import renameSheetDocument from '~/gql/dcis/mutations/sheet/rename_sheet.graphql'
import {
  RenameSheetMutation,
  RenameSheetMutationVariables
} from '~/types/graphql'

/**
 * Мутация для изменения функции
 */
export const useRenameSheetMutation = (
  sheetId: string,
  name: string,
  update?: MutationUpdaterFn) => {
  return useMutation<RenameSheetMutation, RenameSheetMutationVariables>(renameSheetDocument, {
    update,
    variables: { sheetId, name }
  })
}
