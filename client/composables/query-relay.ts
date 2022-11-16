import { DocumentNode } from 'graphql'
import { DataProxy } from '@apollo/client'
import { useQuery } from '@vue/apollo-composable'
import { useScroll } from '@vueuse/core'
import { FetchResult } from '@apollo/client/link/core'
import type {
  DocumentParameter,
  VariablesParameter,
  OptionsParameter,
  UseQueryReturn
} from '@vue/apollo-composable/dist/useQuery'
import type { ComputedRef } from '#app'
import { computed } from '#app'
import { UseResultReturn } from '@vue/apollo-composable/dist/useResult'
import { ExtractSingleKey } from '@vue/apollo-composable/dist/util/ExtractSingleKey'
import { InvariantError } from 'ts-invariant'
import { PageInfo } from '~/types/graphql'
import { getValue } from '~/services/graphql-relay'
import { PaginationInterface, useOffsetPagination } from '~/composables/pagination'
import { useResult } from '~/composables/query-result'

export type ResultDefaultValueType<TNode> = {
  totalCount: number,
  edges: { node: TNode }[],
  pageInfo?: PageInfo
}

export type TransformUpdate<TResultQuery, TResultMutation> = (
  data: TResultQuery,
  result?: Omit<FetchResult<TResultMutation>, 'context'>
) => TResultQuery

export type QueryRelayParams<TResult = any, TVariables = any> = {
  document: DocumentParameter<TResult, TVariables>,
  variables?: VariablesParameter<TVariables>,
  options?: OptionsParameter<TResult, TVariables>
}

export type QueryRelayOptions = {
  pagination: PaginationInterface,
  fetchScroll?: Document | HTMLElement | undefined
  fetchThrottle?: number
}

export type UseResultDefaultValueType<TNode> = { totalCount: number, edges: { node: TNode }[] }

export type QueryRelayResult<
  TResult = any,
  TVariables = any,
  TNode extends { id: string | number } = any
> = UseQueryReturn<TResult, TVariables> & {
  dataQuery: UseResultReturn<UseResultDefaultValueType<TNode> | ExtractSingleKey<NonNullable<TResult>>>
  data: ComputedRef<TNode[]>
  pagination: PaginationInterface
  fetchMoreAvailable: ComputedRef<boolean>
  fetchMoreData: () => void
  update: <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    transform: TransformUpdate<TResult, TResultMutation>
  ) => void
  addUpdate: <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    key?: string | null
  ) => void
  changeUpdate: <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    key?: string | null
  ) => void
  deleteUpdate: <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>
  ) => void
}
export function useQueryRelay<TResult = any, TVariables = any, TNode extends { id: string | number} = any> (
  queryParams: QueryRelayParams<TResult, TVariables>,
  queryOptions: QueryRelayOptions = {
    pagination: useOffsetPagination()
  }
): QueryRelayResult<TResult, TVariables, TNode> {
  const { document, variables, options } = queryParams
  const { pagination, fetchScroll, fetchThrottle } = queryOptions
  /**
   * Переменные запроса
   */
  const queryVariables: ComputedRef<TVariables> = computed<TVariables>(() => {
    return { ...pagination.variables.value, ...getValue<TVariables>(variables) }
  })

  /**
   * Запросы
   */
  const q: UseQueryReturn<TResult, TVariables> = useQuery<TResult, TVariables>(document, queryVariables, options)
  const dataQuery = useResult<TResult, ResultDefaultValueType<any>>(q.result, { totalCount: 0, edges: [] })

  /**
   * Чистые данные
   */
  const data: ComputedRef<TNode[]> = computed<TNode[]>(() => {
    const { totalCount, pageInfo, edges } = (dataQuery.value as unknown as {
      totalCount: number,
      edges: { node: TNode }[],
      pageInfo?: PageInfo
    })
    pagination.setQueryInfo(totalCount, edges.length, pageInfo)
    if (pagination.mode === 'fetch' && pagination.recountPage) {
      pagination.recountPage()
    }
    return edges.map(e => e.node)
  })

  /**
   * Могу ли я подгружать еще записи
   */
  const fetchMoreAvailable: ComputedRef<boolean> = computed<boolean>(() => {
    return pagination.mode === 'fetch' && !q.loading.value && pagination.fetchMore.value
  })
  /**
   * Подгрузка записей
   */
  const fetchMoreData = (): void => {
    if (!fetchMoreAvailable.value) {
      return
    }
    pagination.setPage(++pagination.page.value)
    q.fetchMore({
      variables: { ...getValue(variables), ...pagination.extendVariables.value },
      updateQuery: (previousResult: TResult, { fetchMoreResult }): TResult => {
        return Object.keys(previousResult).reduce((a, key) => ({
          ...a,
          [key as keyof TResult]: {
            __typename: previousResult[key].__typename,
            totalCount: fetchMoreResult[key].totalCount,
            pageInfo: fetchMoreResult[key].pageInfo || undefined,
            edges: [...previousResult[key].edges, ...fetchMoreResult[key].edges]
          }
        }), {}) as TResult
      }
    }).then()
  }

  /**
   * Событие на подгрузку по прокрутке
   */
  const { y } = useScroll(fetchScroll, {
    throttle: fetchThrottle ?? 300,
    onScroll (event: Event | any) {
      if (fetchMoreAvailable.value && y.value + window.innerHeight + 200 > event.target.documentElement.offsetHeight) {
        fetchMoreData()
      }
    }
  })
  /**
   * Обновление при совершении мутации
   * @param cache - хранилище
   * @param result - результат выполнения мутации
   * @param transform - функция преобразования
   * @param isStrict - происходит ли исключение, если запись отсутствует в кеше
   */
  const update = <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    transform: TransformUpdate<TResult, TResultMutation>,
    isStrict: boolean = true
  ): void => {
    try {
      const cacheData: TResult = cache.readQuery<TResult, TVariables>({
        query: document as DocumentNode,
        variables: queryVariables.value
      })
      const data: TResult = transform(cacheData, result)
      cache.writeQuery({ query: document as DocumentNode, variables: queryVariables.value, data })
    } catch (e) {
      if (e instanceof InvariantError && !isStrict) {
        return
      }
      throw e
    }
  }
  /**
   * Получение __typename элементов
   * @param edges - список объектов из списка
   * @param el - манипулируемый объект
   */
  const getEdgeTypename = (edges: { __typename: string }[], el: TNode & { __typename?: string }): string =>
    edges.length === 0 ? `${el.__typename}Edge` : edges[0].__typename
  /**
   * Результат выполнения мутации
   * @param result
   */
  const getMutationResult = (result: any): any => result.data[Object.keys(result.data)[0]]

  /**
   * Обновление запроса при добавлении
   * @param cache - хранилище
   * @param result - результат выполнения мутации
   * @param key - элемент в мутации
   */
  const addUpdate = <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    key: string | null = null
  ): void => {
    update(cache, result, (dataCache) => {
      const mutationResult = getMutationResult(result)
      return Object.keys(dataCache).reduce((a, k) => {
        const kdm: string = key === null ? k : key
        return {
          ...a,
          [k as keyof TResult]: {
            ...dataCache[k],
            totalCount: dataCache[k].totalCount + (Array.isArray(mutationResult[kdm]) ? mutationResult[kdm].length : 1),
            edges: [
              ...(Array.isArray(mutationResult[kdm])
                ? mutationResult[kdm].map((el: TNode) => ({
                  node: el,
                  __typename: getEdgeTypename(dataCache[k].edges, el)
                }))
                : [{ node: mutationResult[kdm], __typename: getEdgeTypename(dataCache[k].edges, mutationResult[kdm]) }]
              ),
              ...dataCache[k].edges
            ]
          }
        }
      }, {}) as TResult
    })
  }

  /**
   * Изменение при редактировании записи
   * @param cache - хранилище
   * @param result - результат выполнения мутации
   * @param key - элемент в мутации
   */
  const changeUpdate = <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    key: string | null = null
  ): void => {
    update(cache, result, (dataCache) => {
      const k: string = Object.keys(dataCache)[0]
      const mutationResult = getMutationResult(result)
      const node: TNode = mutationResult[key === null ? k : key]
      if (node) {
        dataCache[k].edges.find((el: { node: TNode }) => el.node.id === node.id).node = Object.assign(
          dataCache[k].edges.find((el: { node: TNode }) => el.node.id === node.id).node,
          node
        )
      }
      return dataCache
    })
  }

  /**
   * Удаление записи
   * @param cache - хранилище
   * @param result - результат выполнения мутации
   * @param isStrict - происходит ли исключение, если запись отсутствует в кеше
   */
  const deleteUpdate = <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    isStrict: boolean = true
  ): void => {
    update(cache, result, (dataCache) => {
      const { id } = getMutationResult(result)
      if (id) {
        const k: string = Object.keys(dataCache)[0]
        dataCache[k].edges = dataCache[k].edges.filter((el: { node: TNode }) => el.node.id !== id)
        --dataCache[k].totalCount
      }
      return dataCache
    }, isStrict)
  }

  return {
    ...q,
    dataQuery,
    data,
    pagination,
    fetchMoreAvailable,
    fetchMoreData,
    update,
    addUpdate,
    changeUpdate,
    deleteUpdate
  }
}
