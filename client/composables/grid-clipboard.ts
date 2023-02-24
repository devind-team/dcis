import Vue from 'vue'
import { inject, Ref } from '#app'
import { useEventListener } from '@vueuse/core'
import { CellPasteStyleInputType, CellType, ColumnDimensionType, RowDimensionType, SheetType } from '~/types/graphql'
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
  style: CellPasteStyleInputType | null
}

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

  useEventListener(
    typeof document === 'undefined' ? null : document,
    'paste',
    async (event: ClipboardEvent) => {
      if (
        event.target instanceof HTMLInputElement ||
        event.target instanceof HTMLTextAreaElement ||
        (mode.value !== GridMode.WRITE && mode.value !== GridMode.CHANGE) ||
        selectedCells.value.length === 0
      ) {
        return
      }
      let textData: string | null
      let htmlData: string | null
      if (event.clipboardData) {
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
      const table = htmlData.includes('<table')
        ? parseHTMLTable(htmlData, mode.value === GridMode.CHANGE)
        : parsePlainTextTable(textData)
      const values = getTablesIntersection(selectedCells.value, activeSheet.value, table)
        .filter((value: ValueStyleInputType) => canChangeValue(value.cell) && value.cell.kind !== 'fl')
      await paste(values)
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

  const generateHTMLTable = (selectedCells: CellType[]): string => {
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
        { props: { selectedCells: cells, getColumnWidth, getRowHeight, activeSheet: activeSheet.value } }
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
        table.at(-1).push({ value, style: null })
      }
    }
    return table
  }

  const parseHTMLTable = (htmlTable: string, withStyles: boolean): TableCellType[][] => {
    const iframe = document.createElement('iframe')
    document.body.append(iframe)
    const doc = iframe.contentDocument
    doc.open()
    doc.write(htmlTable)
    doc.close()
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
          style: withStyles ? getCellStyles(cell, iframe.contentWindow) : null
        }
        columnIndex += cell.colSpan
      }
    }
    iframe.remove()
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
            result.push({ cell, value: tableCell.value, style: tableCell.style })
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

  const getCellStyles = (cell: HTMLTableCellElement, contentWindow: Window): CellPasteStyleInputType => {
    const computedStyle = contentWindow.getComputedStyle(cell)
    const s = cell.querySelector('s')
    const horizontalAlign = {
      left: 'left',
      center: 'center',
      right: 'right',
      start: 'left',
      end: 'right',
      '-webkit-right': 'right'
    }
    return {
      strong: computedStyle.fontWeight === 'bold' || parseInt(computedStyle.fontWeight) >= 700,
      italic: computedStyle.fontStyle === 'italic',
      underline: computedStyle.textDecorationLine === 'underline' ? 'single' : null,
      strike: s !== null || computedStyle.textDecoration.includes('line-through'),
      horizontalAlign: horizontalAlign[computedStyle.textAlign] ?? 'left',
      verticalAlign: computedStyle.verticalAlign,
      size: Math.round(parseFloat(computedStyle.fontSize) * 0.75)
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
