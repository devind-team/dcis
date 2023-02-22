import Vue from 'vue'
import { inject, Ref } from '#app'
import { useEventListener } from '@vueuse/core'
import { CellType, ColumnDimensionType, RowDimensionType, SheetType } from '~/types/graphql'
import { ValueStyleInputType } from '~/composables/grid-mutations'
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

type TableCellType = {
  value: string,
  styles: Record<string, string>
}

export function useGridClipboard (
  selectedCells: Ref<CellType[]>,
  getColumnWidth: (column: ColumnDimensionType) => number,
  getRowHeight: (row: RowDimensionType) => number
) {
  const mode = inject(GridModeInject)
  const activeSheet = inject(ActiveSheetInject)
  const canChangeValue = useCanChangeValue()
  const { paste, pasteWithStyles } = usePaste()

  const copyHandler = async (event: Event, withStyles: boolean) => {
    if (
      event.target instanceof HTMLInputElement ||
      event.target instanceof HTMLTextAreaElement ||
      selectedCells.value.length === 0
    ) {
      return
    }
    const text = generatePlainTextTable(selectedCells.value)
    const html = generateHTMLTable(selectedCells.value, withStyles)
    if (event instanceof ClipboardEvent && event.clipboardData) {
      event.clipboardData.clearData()
      event.clipboardData.setData('text/plain', text)
      event.clipboardData.setData('text/html', html)
    } else {
      await navigator.clipboard.write([new ClipboardItem({
        'text/plain': new Blob([text], { type: 'text/plain' }),
        'text/html': new Blob([html], { type: 'text/html' })
      })])
    }
    event.preventDefault()
  }

  const pasteHandler = async (event: Event, withStyles: boolean) => {
    if (
      event.target instanceof HTMLInputElement ||
      event.target instanceof HTMLTextAreaElement ||
      (mode.value !== GridMode.WRITE && mode.value !== GridMode.CHANGE) ||
      selectedCells.value.length === 0
    ) {
      return
    }
    let textData: string | null = null
    let htmlData: string | null = null
    if (event instanceof ClipboardEvent && event.clipboardData) {
      textData = event.clipboardData.getData('text/plain')
      htmlData = event.clipboardData.getData('text/html')
    } else {
      textData = await navigator.clipboard.readText()
      const items = await navigator.clipboard.read()
      const item = items.find((item: ClipboardItem) => item.types.includes('text/html'))
      const blob = await item.getType('text/html')
      htmlData = await blob.text()
    }
    if (htmlData === '' && textData === '') {
      return
    }
    const table = htmlData.includes('<table') ? parseHTMLTable(htmlData, withStyles) : parsePlainTextTable(textData)
    const values = getTablesIntersection(selectedCells.value, activeSheet.value, table)
      .filter((value: ValueStyleInputType) => canChangeValue(value.cell) && value.cell.kind !== 'fl')
    if (withStyles) {
      pasteWithStyles(values)
    } else {
      paste(values)
    }
  }

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'copy',
    async (event: ClipboardEvent) => {
      await copyHandler(event, false)
    }
  )

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'copy-with-styles',
    async (event: CustomEvent) => {
      await copyHandler(event, true)
    }
  )

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'paste',
    async (event: ClipboardEvent) => {
      await pasteHandler(event, false)
    }
  )

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'paste-with-styles',
    async (event: ClipboardEvent) => {
      await pasteHandler(event, true)
    }
  )

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

  const generateHTMLTable = (selectedCells: CellType[], withStyles: boolean): string => {
    const { minColumn, minRow, maxColumn, maxRow } = positionsToRangeIndices(getRelatedGlobalPositions(selectedCells))
    const cells: CellType[][] = []
    for (let row = minRow; row <= maxRow; row++) {
      cells.push([])
      for (let column = minColumn; column <= maxColumn; column++) {
        const position = `${positionToLetter(column)}${row}`
        const cell = selectedCells.find((cell: CellType) => cell.globalPosition === position)
        if (cell) {
          cells.at(-1).push(cell)
        }
      }
    }
    const vm = new Vue({
      render: h => h(
        ClipboardTable,
        { props: { selectedCells: cells, getColumnWidth, getRowHeight, activeSheet: activeSheet.value, withStyles } }
      )
    })
    return `
      <!DOCTYPE html>
      ${vm.$mount().$el.outerHTML}
    `
  }

  const parsePlainTextTable = (textTable: string): TableCellType[][] => {
    const table: TableCellType[][] = []
    for (const row of textTable.split(getEndOfLine())) {
      if (row === '') {
        break
      }
      table.push([])
      for (const value of row.split('\t')) {
        table.at(-1).push({ value, styles: {} })
      }
    }
    return table
  }

  const parseHTMLTable = (htmlTable: string, withStyles: boolean): TableCellType[][] => {
    const parser = new DOMParser()
    const doc = parser.parseFromString(htmlTable, 'text/html')
    const tableElement = doc.querySelector('table')
    const columnsNumber = getColumnsNumber(tableElement)
    const table: TableCellType[][] = Array.from(
      { length: tableElement.rows.length },
      () => new Array(columnsNumber).fill({ value: '', styles: {} })
    )
    for (let rowIndex = 0; rowIndex < tableElement.rows.length; rowIndex++) {
      let columnIndex = 0
      for (const cell of tableElement.rows[rowIndex].cells) {
        table[rowIndex][columnIndex] = {
          value: cell.innerText,
          styles: withStyles ? getCellStyles(cell) : {}
        }
        columnIndex += cell.colSpan
      }
    }
    return table
  }

  const getTablesIntersection = (
    selectedCells: CellType[],
    activeSheet: SheetType,
    table: TableCellType[][]
  ): ValueStyleInputType[] => {
    const result: ValueStyleInputType[] = []
    const startPosition = parsePosition(selectedCells[0].globalPosition)
    const columnIndex = letterToPosition(startPosition.column)
    const rowIndex = startPosition.row
    for (let i = 0; i < table.length; i++) {
      const row = table[i]
      for (let j = 0; j < row.length; j++) {
        const tableCell = row[j]
        if (tableCell) {
          const position = `${positionToLetter(columnIndex + j)}${rowIndex + i}`
          const cell = findCell(activeSheet, (cell: CellType) => cell.globalPosition === position)
          if (cell) {
            result.push({ cell, value: tableCell.value, styles: tableCell.styles })
          }
        }
      }
    }
    return result
  }

  const getColumnsNumber = (table: HTMLTableElement): number => {
    let result = 0
    for (const row of table.rows) {
      let columnIndex = 0
      for (const cell of row.cells) {
        columnIndex += cell.colSpan
      }
      if (columnIndex > result) {
        result = columnIndex
      }
    }
    return result
  }

  const getCellStyles = (cell: HTMLTableCellElement): Record<string, string> => {
    return {
      strong: getComputedStyle(cell).fontWeight === 'bold' ? 'true' : 'false',
      italic: getComputedStyle(cell).fontStyle === 'italic' ? 'true' : 'false',
      strike: getComputedStyle(cell).textDecoration === 'line-through' ? 'true' : 'false',
      underline: getComputedStyle(cell).textDecorationLine || null,
      horizontal_align: getComputedStyle(cell).textAlign,
      vertical_align: getComputedStyle(cell).verticalAlign,
      size: getComputedStyle(cell).fontSize
    }
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
