import { useMutation } from '@vue/apollo-composable'
import {
  ChangeColumnDimensionMutation,
  ChangeColumnDimensionMutationVariables,
  ColumnDimensionType
} from '~/types/graphql'
import changeColumnDimension from '~/gql/dcis/mutations/sheet/change_column_dimension.graphql'

export function useGridMutations () {
  const changeColumnWidth = async (columnDimension: ColumnDimensionType, width: number) => {
    const { mutate } = useMutation<ChangeColumnDimensionMutation, ChangeColumnDimensionMutationVariables>(
      changeColumnDimension
    )
    return await mutate({
      id: columnDimension.id,
      width,
      fixed: columnDimension.fixed,
      hidden: columnDimension.hidden,
      autoSize: columnDimension.autoSize
    })
  }

  return {
    changeColumnWidth
  }
}
