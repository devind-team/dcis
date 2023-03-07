/**
 * Сервис для выделения ячейки с последующей передачей управления другому элементу
 */

import { EventEmitter } from 'events'
import { computed, ComputedRef, Ref, ref, unref } from '#app'
import { CellsOptionsType, GridMode } from '~/types/grid'
import { CellType, SheetType } from '~/types/graphql'

export const START_CHOICE_EVENT = Symbol('startChoice')
export const END_CHOICE_EVENT = Symbol('endChoice')
export const CANCEL_EVENT = Symbol('cancel')

export type GridChoiceType = {
  active: ComputedRef<boolean>
  text: ComputedRef<string>
  targetCell: Ref<CellType>,
  sheetIndex: Ref<number>,
  startChoice: (name: string, cell: CellType, activeSheetIndex: number) => void,
  endChoice: () => void
  cancel: () => void
  on: (eventName: string | symbol, listener: (...args: any[]) => void) => EventEmitter
  removeListener: (eventName: string | symbol, listener: (...args: any[]) => void) => EventEmitter
}

export type CancelEventType = {
  targetCell: CellType
  sheetIndex: number
  controlName: string
}

export type EndChoiceEventType = CancelEventType & {
  cells: CellType[]
}

export function useGridChoice (
  mode: GridMode,
  sheet: ComputedRef<SheetType | null>,
  selectedCellsOptions: ComputedRef<CellsOptionsType>
) {
  const eventEmitter = new EventEmitter()

  const currentChoice = ref<boolean>(false)
  const active = computed<boolean>(() => (
    currentChoice.value && mode === GridMode.CHANGE && Boolean(unref(sheet))
  ))

  const targetCell = ref<CellType | null>(null)
  const sheetIndex = ref<number | null>(null)
  const controlName = ref<string | null>(null) // Необходимо для адресации компонентов в будущем

  const startChoice = (name: string, cell: CellType, activeSheetIndex: number) => {
    controlName.value = name
    targetCell.value = cell
    sheetIndex.value = activeSheetIndex
    currentChoice.value = true
  }

  /**
   * Заканчиваем процесс выделения, вызываем emit для оповещения подписчиков
   */
  const endChoice = () => {
    eventEmitter.emit(END_CHOICE_EVENT, {
      targetCell: unref(targetCell),
      sheetIndex: unref(sheetIndex),
      controlName: unref(controlName),
      cells: unref(selectedCellsOptions).cells
    } as EndChoiceEventType)
    close()
  }

  const cancel = () => {
    eventEmitter.emit(CANCEL_EVENT, {
      targetCell: unref(targetCell),
      sheetIndex: unref(sheetIndex),
      controlName: unref(controlName)
    } as CancelEventType)
    close()
  }

  const close = () => {
    targetCell.value = null
    sheetIndex.value = null
    controlName.value = null
    currentChoice.value = false
  }

  const on = (eventName: string | symbol, listener: (...args: any[]) => void): EventEmitter =>
    eventEmitter.on(eventName, listener)
  const removeListener = (eventName: string | symbol, listener: (...args: any[]) => void): EventEmitter =>
    eventEmitter.removeListener(eventName, listener)

  const text = computed<string>(() => {
    if (unref(sheet) && unref(selectedCellsOptions)) {
      return `${unref(sheet).name}!` +
          unref(selectedCellsOptions).cells.map<string>((cell: CellType) => cell.position).join(',')
    }
    return '-'
  })

  return {
    active,
    text,
    targetCell,
    sheetIndex,
    on,
    removeListener,
    startChoice,
    endChoice,
    cancel
  }
}
