import type { ComputedRef } from '#app'
import { computed } from '#app'
import { useQueryRelay } from './query-relay'
import { CategoriesQuery, CategoriesQueryVariables, CategoryType } from '~/types/graphql'
import categoriesQuery from '~/gql/pages/queries/categories.graphql'

export function usePage () {
  const { data: categories } = useQueryRelay<CategoriesQuery, CategoriesQueryVariables, CategoryType>({
    document: categoriesQuery,
    variables: { isNull: true }
  })

  const flatCategories: ComputedRef<CategoryType[]> = computed<CategoryType[]>(() => {
    const children = categories.value.reduce((a, c) => ([...a, ...c.children]), [])
    return [...categories.value, ...children]
  })

  return { flatCategories }
}
