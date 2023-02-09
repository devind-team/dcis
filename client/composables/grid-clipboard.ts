import Vue from 'vue'
import { inject, Ref } from '#app'
import { useEventListener } from '@vueuse/core'
import { CellType, ColumnDimensionType, RowDimensionType, SheetType } from '~/types/graphql'
import { ValueInputType } from '~/composables/grid-mutations'
import {
  findCell,
  getRelatedGlobalPositions,
  letterToPosition,
  parsePosition,
  positionsToRangeIndices,
  positionToLetter
} from '~/services/grid'
import { ActiveSheetInject, GridMode, GridModeInject } from '~/types/grid'
import { usePaste } from '~/composables/grid-actions'
import { useCanChangeValue } from '~/composables/grid-permissions'
import ClipboardTable from '~/components/dcis/grid/clipboard/ClipboardTable.vue'

export function useGridClipboard (
  selectedCells: Ref<CellType[]>,
  getColumnWidth: (column: ColumnDimensionType) => number,
  getRowHeight: (row: RowDimensionType) => number
) {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const canChangeValue = useCanChangeValue()
  const paste = usePaste()

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'paste',
    async (event: ClipboardEvent) => {
      const data = event.clipboardData.getData('text/plain')
      if (
        event.target instanceof HTMLInputElement ||
        event.target instanceof HTMLTextAreaElement ||
        mode.value !== GridMode.WRITE ||
        selectedCells.value.length === 0 ||
        data === ''
      ) {
        return
      }
      const table = parsePlainTextTable(data)
      const values = getTablesIntersection(selectedCells.value, activeSheet.value, table)
        .filter((value: ValueInputType) => canChangeValue(value.cell) && value.cell.kind !== 'fl')
      await paste(values)
    }
  )

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'copy',
    (event: ClipboardEvent) => {
      if (
        event.target instanceof HTMLInputElement ||
        event.target instanceof HTMLTextAreaElement ||
        selectedCells.value.length === 0
      ) {
        return
      }
      event.clipboardData.clearData()
      event.clipboardData.setData('text/plain', generatePlainTextTable(selectedCells.value))
      event.clipboardData.setData('text/html', generateHTMLTable(selectedCells.value))
      event.preventDefault()
    }
  )

  const parsePlainTextTable = (textTable: string): string[][] => {
    const table: string[][] = []
    for (const row of textTable.split(getEndOfLine())) {
      if (row === '') {
        break
      }
      table.push([])
      for (const cell of row.split('\t')) {
        table.at(-1).push(cell)
      }
    }
    return table
  }

  const generatePlainTextTable = (selectedCells: CellType[]): string => {
    const { minColumn, minRow, maxColumn, maxRow } = positionsToRangeIndices(getRelatedGlobalPositions(selectedCells))
    const endOfLine = getEndOfLine()
    let result = ''
    for (let row = minRow; row <= maxRow; row++) {
      for (let column = minColumn; column <= maxColumn; column++) {
        const position = `${positionToLetter(column)}${row}`
        const cell = selectedCells.find((cell: CellType) => cell.globalPosition === position)
        if (cell) {
          result += cell.value
        }
        if (column !== maxColumn) {
          result += '\t'
        }
      }
      result += endOfLine
    }
    return result
  }

  const generateHTMLTable = (selectedCells: CellType[]): string => {
    const cells: CellType[][] = []
    let rowId = ''
    for (const cell of selectedCells) {
      if (cell.rowId !== rowId) {
        cells.push([])
        rowId = cell.rowId
      }
      cells.at(-1).push(cell)
    }
    const vm = new Vue({
      render: h => h(
        ClipboardTable,
        { props: { selectedCells: cells, getColumnWidth, getRowHeight, activeSheet: activeSheet.value } }
      )
    })
    return `
      <!DOCTYPE html>
      ${vm.$mount().$el.outerHTML}
    `
  }

  const getTablesIntersection = (
    selectedCells: CellType[],
    activeSheet: SheetType,
    table: string[][]
  ): ValueInputType[] => {
    const result: ValueInputType[] = []
    const startPosition = parsePosition(selectedCells[0].globalPosition)
    const columnIndex = letterToPosition(startPosition.column)
    const rowIndex = startPosition.row
    for (let i = 0; i < table.length; i++) {
      const row = table[i]
      for (let j = 0; j < row.length; j++) {
        const value = row[j]
        if (value) {
          const position = `${positionToLetter(columnIndex + j)}${rowIndex + i}`
          const cell = findCell(activeSheet, (cell: CellType) => cell.globalPosition === position)
          if (cell) {
            result.push({ cell, value })
          }
        }
      }
    }
    return result
  }

  const getEndOfLine = (): string => {
    if (!navigator) {
      return '\n'
    }
    if (navigator.userAgent.includes('Windows')) {
      return '\r\n'
    } else if (navigator.userAgent.includes('Mac')) {
      return '\r'
    } else {
      return '\n'
    }
  }
}
