import { computed } from '#app'
import type { ComputedRef } from '#app'
import type { BuildColumnType, BuildRowType, BuildCellType, SheetType } from '~/types/dcis'
import { positionToLetter } from '~/services/grid'

export function useGrid (sheet: ComputedRef<SheetType>) {
  const columns: ComputedRef<BuildColumnType[]> = computed<BuildColumnType[]>(() => {
    const result: BuildColumnType[] = []
    for (let i = 0; i < sheet.value.columnsCount; i++) {
      let style: Record<string, string> = {}
      if (sheet.value.columnsDimension[i]) {
        style = {
          width: `${sheet.value.columnsDimension[i].width}px`
        }
      }
      result.push({
        name: positionToLetter(i + 1),
        style
      })
    }
    return result
  })
  const rows: ComputedRef<BuildRowType[]> = computed<BuildRowType[]>(() => {
    const result: BuildRowType[] = []
    for (let i = 0; i < sheet.value.rowsCount; i++) {
      const rowIndex = i + 1
      let style: Record<string, string> = {}
      if (sheet.value.rowsDimension[i]) {
        style = {
          height: `${sheet.value.rowsDimension[i].height}px`
        }
      }
      const row: BuildRowType = {
        rowIndex,
        buildCells: [],
        style,
        originRow: sheet.value.rows[i]
      }
      for (let j = 0; j < sheet.value.columnsCount; j++) {
        const columnIndex = j + 1
        const position = `${positionToLetter(columnIndex)}${rowIndex}`
        const cell: BuildCellType = {
          columnIndex,
          position,
          colspan: 1,
          rowspan: 1,
          originCell: sheet.value.rows[i].cells[j]
        }
        if (position in sheet.value.mergeCells) {
          row.buildCells.push({ ...cell, ...sheet.value.mergeCells[position] })
        } else {
          row.buildCells.push(cell)
        }
      }
      result.push(row)
    }
    return result
  })
  return { columns, rows }
}
