import defu from 'defu'
import type { Ref, ComputedRef } from '#app'
import { useState, computed } from '#app'
import { PageInfo } from '~/types/graphql'
import { cursor } from '~/services/graphql-relay'

export type PaginationMode = 'fetch' | 'paged'
export type PaginationOptions = { page?: number, pageSize?: number, mode?: PaginationMode }
export type PaginationVariablesType = { first: number, offset?: number, after?: string }
export interface PaginationInterface {
  mode: PaginationMode,
  page: Ref<number>
  setPage: (p: number) => void,
  pageSize: Ref<number>
  count: Ref<number>
  totalCount: Ref<number>
  setQueryInfo: (tc: number, c: number, pi?: PageInfo) => void
  fetchMore: ComputedRef<boolean>
  variables: ComputedRef<PaginationVariablesType>
  extendVariables: ComputedRef<PaginationVariablesType>
  recountPage?: () => void
  pageInfo?: Ref<PageInfo>
}

/**
 * Пагинация, основанная на offset подходе
 * @param paginationOptions
 */
export function useOffsetPagination (paginationOptions: PaginationOptions = {}): PaginationInterface {
  const defaultOptions: PaginationOptions = {
    page: 1,
    pageSize: 30,
    mode: 'fetch'
  }
  const options: PaginationOptions = defu(paginationOptions, defaultOptions)

  const page: Ref<number> = useState<number>('page', () => options.page)
  const pageSize: Ref<number> = useState('pageSize', () => options.pageSize)
  const count: Ref<number> = useState('count', () => 0)
  const totalCount: Ref<number> = useState('totalCount', () => 0)

  const extendVariables: ComputedRef<PaginationVariablesType> = computed(() => ({
    first: pageSize.value,
    offset: (page.value - 1) * pageSize.value
  }))

  /**
   * Расширение переменных в зависимости от типа пагинации
   */
  const variables: ComputedRef<PaginationVariablesType> = options.mode === 'fetch'
    ? computed<PaginationVariablesType>(() => ({
      first: pageSize.value,
      offset: 0
    }))
    : extendVariables

  const fetchMore: ComputedRef<boolean> = computed<boolean>(() => {
    return page.value * pageSize.value < totalCount.value
  })
  /**
   * Пересчитываем значение позиции страницы
   */
  const recountPage = (): void => {
    page.value = Math.ceil(count.value / pageSize.value)
  }
  /**
   * Устанавливаем новую страницу
    * @param p
   */
  const setPage = (p: number = 1): void => {
    page.value = p
  }
  /**
   * Устанаваливаем количество записей
   * @param tc - totalCount
   * @param c - count
   */
  const setQueryInfo = (tc: number, c: number): void => {
    count.value = c
    totalCount.value = tc
  }

  return {
    mode: options.mode,
    page,
    pageSize,
    totalCount,
    count,
    fetchMore,
    variables,
    extendVariables,
    setPage,
    setQueryInfo,
    recountPage
  }
}

/**
 * Пагинация, основанная на cursor подходе
 * @param paginationOptions
 */
export function useCursorPagination (paginationOptions: PaginationOptions = {}): PaginationInterface {
  const {
    page,
    setPage,
    pageSize,
    mode,
    totalCount,
    count,
    setQueryInfo: setQueryInfoParent
  } = useOffsetPagination(paginationOptions)

  const pageInfo: Ref<PageInfo> = useState('pageInfo', () => ({
    hasPreviousPage: true,
    hasNextPage: true
  }))

  const variables: ComputedRef<PaginationVariablesType> = computed<PaginationVariablesType>(() => ({
    first: pageSize.value
  }))

  const extendVariables: ComputedRef<PaginationVariablesType> = computed<PaginationVariablesType>(() => ({
    first: pageSize.value,
    after: cursor(count.value - 1)
  }))

  const fetchMore: ComputedRef<boolean> = computed<boolean>(() => {
    return pageInfo.value.hasNextPage
  })

  /**
   * Устанаваливаем количество записей
   * @param tc - totalCount
   * @param c - количество записей
   * @param pi - pageInfo
   */
  const setQueryInfo = (tc: number, c: number, pi: PageInfo): void => {
    setQueryInfoParent(tc, c)
    pageInfo.value = pi
  }

  return {
    mode,
    page,
    pageSize,
    totalCount,
    count,
    fetchMore,
    variables,
    extendVariables,
    pageInfo,
    setPage,
    setQueryInfo
  }
}
