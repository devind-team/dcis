import type { ComputedRef, Ref } from '#app'
import { computed, ref } from '#app'

import type { CellType, ColumnDimensionType, MergedCellType, SheetType, ValueType } from '~/types/graphql'

import { getCellBorder, getCellStyle, getCellValue, positionToLetter } from '~/services/grid'
import { BuildCellType, BuildColumnType, BuildRowType } from '~/types/grid-types'

export const cellKinds: Record<string, string> = {
  n: 'Numeric',
  s: 'String',
  text: 'Text',
  money: 'Money',
  department: 'Department'
}

export function useGrid (sheet: Ref<SheetType>) {
  const columns: ComputedRef<BuildColumnType[]> = computed<BuildColumnType[]>(() => (
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => ({
      id: columnDimension.id,
      index: columnDimension.index,
      positional: positionToLetter(columnDimension.index),
      style: {
        width: columnDimension.width ? `${columnDimension.width}px` : '60px'
      },
      dimension: columnDimension
    }))
  ))

  /**
   * Собираем структуру для быстрого поиска
   */
  const cells: ComputedRef = computed(() => {
    const buildCells = {}
    for (const cell of sheet.value.cells) {
      if (!(cell.rowId in buildCells)) {
        buildCells[cell.rowId] = {}
      }
      buildCells[cell.rowId][cell.columnId] = cell
    }
    return buildCells
  })

  /**
   * Формируем значения
   */
  const values: ComputedRef = computed(() => {
    const buildValues = {}
    for (const value of sheet.value.values) {
      if (!(value.rowId in buildValues)) {
        buildValues[value.rowId] = {}
      }
      buildValues[value.rowId][value.columnId] = value
    }
    return buildValues
  })

  const rows: ComputedRef<BuildRowType[]> = computed<BuildRowType[]>(() => {
    const buildRows: BuildRowType[] = []
    for (let rowIndex = 0; rowIndex < sheet.value.rows.length; ++rowIndex) {
      const row = sheet.value.rows[rowIndex]
      const buildRow: BuildRowType = {
        sheetId: sheet.value.id,
        id: row.id,
        index: row.index,
        dynamic: row.dynamic,
        style: {
          height: row.height ? `${row.height}px` : undefined
        },
        cells: [],
        dimension: row
      }
      const rowCells = cells.value[row.id]
      const valueCells = row.id in values.value ? values.value[row.id] : null
      for (let columnIndex = 0; columnIndex < sheet.value.columns.length; ++columnIndex) {
        const column: ColumnDimensionType = sheet.value.columns[columnIndex]
        const cell: CellType = rowCells[column.id]
        const value: ValueType | null = valueCells && column.id in valueCells ? valueCells[column.id] : null
        const position: string = `${positionToLetter(column.index)}${row.index}`
        const buildCell: BuildCellType = {
          sheetId: sheet.value.id,
          id: cell.id,
          position,
          value: getCellValue(value, cell),
          editable: cell.editable,
          kind: cell.kind,
          colspan: 1,
          rowspan: 1,
          style: getCellStyle(cell),
          border: getCellBorder(cell),
          cell
        }
        if (position in mergeCells.value) {
          buildRow.cells.push(Object.assign(buildCell, mergeCells.value[position]))
        } else if (!mergedCells.value.includes(position)) {
          buildRow.cells.push(buildCell)
        }
      }
      buildRows.push(buildRow)
    }
    return buildRows
  })

  const mergeCells: ComputedRef = computed(() => (
    sheet.value.mergedCells.reduce((a, c: MergedCellType) => ({ ...a, [c.target]: c }), {})
  ))

  const mergedCells: ComputedRef<string[]> = computed(() => {
    return Object.values<MergedCellType>(sheet.value.mergedCells)
      .reduce<string[]>((a: string[], c: MergedCellType) => ([...a, ...c.cells]), [])
  })

  /**
   * Блок выделения
   */
  const active: Ref<string | null> = ref<string | null>(null)

  const setActive = (position: string, dbl: boolean = false) => {
    active.value = position
    // if (active.value === null && dbl) {
    //   active.value = position
    // } else if (active.value !== position) {
    //   active.value = null
    // }
  }

  return {
    sheet,
    cells,
    columns,
    rows,
    values,
    mergeCells,
    mergedCells,
    active,
    setActive
  }
}
