import { DocumentNode } from 'graphql'
import { DataProxy } from '@apollo/client'
import { UseQueryReturn } from '@vue/apollo-composable/dist/useQuery'
import { FetchResult } from '@apollo/client/link/core'
import { useQuery } from '@vue/apollo-composable'
import { InvariantError } from 'ts-invariant'
import { QueryRelayParams, TransformUpdate } from '~/composables/query-relay'
import { getValue } from '~/services/graphql-relay'
import { useResult } from '~/composables/query-result'

export function useCommonQuery<
  TResult = any,
  TVariables = any,
  TResultKey extends keyof NonNullable<TResult> = keyof NonNullable<TResult>
> (
  queryParams: QueryRelayParams<TResult, TVariables>
) {
  const { document, variables, options } = queryParams
  /**
   * Запрос на сервер
   */
  const q: UseQueryReturn<TResult, TVariables> = useQuery<TResult, TVariables>(document, variables, options)
  const data = useResult<TResult, TResultKey>(q.result)
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
      const variablesValue = getValue<TVariables>(variables)
      const cacheData: TResult = cache.readQuery<TResult, TVariables>({
        query: document as DocumentNode,
        variables: variablesValue
      })
      const data: TResult = transform(cacheData, result)
      cache.writeQuery({ query: document as DocumentNode, variables: variablesValue, data })
    } catch (e) {
      if (e instanceof InvariantError && !isStrict) {
        return
      }
      throw e
    }
  }
  /**
   * Получение данных результата выполнения мутации
   * @param result - результат выполнения мутации
   */
  const getMutationResult = (result: any): any => result.data[Object.keys(result.data)[0]]
  /**
   * Обновление запроса при добавлении
   * @param cache - хранилище
   * @param result - результат выполнения мутации
   * @param key - элемент в мутации
   * @param start - добавление элемента в начало
   */
  const addUpdate = <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>,
    key: string | null = null,
    start: boolean = true
  ): void => {
    update(cache, result, (dataCache) => {
      const mutationResult = getMutationResult(result)
      const dataKey = Object.keys(dataCache)[0]
      const data = Array.isArray(mutationResult[key]) ? mutationResult[key] : [mutationResult[key]]
      dataCache[dataKey] = start ? [...data, ...dataCache[dataKey]] : [...dataCache[dataKey], ...data]
      return dataCache
    })
  }
  /**
   * Обновление запроса при изменении
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
      const mutationResult = getMutationResult(result)
      const dataKey = Object.keys(dataCache)[0]
      if (Array.isArray(dataCache[dataKey])) {
        const index: number = dataCache[dataKey].findIndex((e: any) => e.id === mutationResult[key].id)
        dataCache[dataKey].splice(index, 1, mutationResult[key])
      } else {
        dataCache[dataKey] = Object.assign(dataCache[dataKey], mutationResult[key])
      }
      return dataCache
    })
  }
  /**
   * Замена записей на новые
   * @param cache - хранилище
   * @param result - результат выполнения мутации
   */
  const resetUpdate = <TResultMutation>(
    cache: DataProxy,
    result: Omit<FetchResult<TResultMutation>, 'context'>
  ): void => {
    update(cache, result, (dataCache) => {
      const mutationResult = getMutationResult(result)
      const dataKey = Object.keys(dataCache)[0]
      dataCache[dataKey] = mutationResult[dataKey]
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
        const dataKey = Object.keys(dataCache)[0]
        dataCache[dataKey] = dataCache[dataKey].filter((e: any) => e.id !== id)
      }
      return dataCache
    }, isStrict)
  }

  return {
    ...q,
    data,
    update,
    addUpdate,
    changeUpdate,
    resetUpdate,
    deleteUpdate
  }
}

export type UpdateType<TResult = any> = <TResultMutation>(
  cache: DataProxy,
  result: Omit<FetchResult<TResultMutation>, 'context'>,
  transform: TransformUpdate<TResult, TResultMutation>
) => void
export type AddUpdateType = ReturnType<typeof useCommonQuery>['addUpdate']
export type ChangeUpdateType = ReturnType<typeof useCommonQuery>['changeUpdate']
export type ResetUpdateType = ReturnType<typeof useCommonQuery>['resetUpdate']
export type DeleteUpdateType = ReturnType<typeof useCommonQuery>['deleteUpdate']
