import { VariablesParameter } from '@vue/apollo-composable/dist/useQuery'
import { ReactiveFunction } from '@vue/apollo-composable/dist/util/ReactiveFunction'
import { ComputedRef, isRef, WritableComputedRef } from '#app'

/**
 * Преобразовываем тип и идентификатор в relayId
 * @param type
 * @param id
 */
export const toGlobalId = (type: string, id: number): string => {
  return Buffer.from(`${type}:${id}`).toString('base64')
}

export type VT<T> = T | ReactiveFunction<T> | ComputedRef<T> | WritableComputedRef<T> | VariablesParameter<T>

/**
 * Распаковываем значение в зависимости от типа
 * @param variables
 */
export function getValue<T> (variables: VT<T>): T {
  if (isRef<T>(variables)) {
    return variables.value
  } else if (typeof variables === 'function') {
    return (variables as ReactiveFunction<T>)()
  }
  return variables
}

/**
 * Преобразовываем relayId в тип и идентификатор
 * @param relayId
 */
export const fromGlobalId = (relayId: string): { type: string, id: number } => {
  const globalIdParts: string[] = Buffer.from(relayId, 'base64').toString().split(':')
  return {
    type: globalIdParts[0],
    id: parseInt(globalIdParts[1])
  }
}

/**
 * Преобразовываем идентификатор позиции
 * @param n
 */
export const cursor = (n: number): string => {
  return Buffer.from(`arrayconnection:${n}`).toString('base64')
}
