import defu from 'defu'
import type { Ref, ComputedRef } from '#app'
import { computed, ref, isRef } from '#app'

import {GridMode, RangePositionsType} from '~/types/grid-types'
import {
  SheetType,
  ColumnDimensionType,
  RowDimensionType,
  MergedCellType,
  CellType,
  ValueType
} from '~/types/graphql'

import {letterToPosition, normalizationRange, parseRangeToPosition, positionToLetter} from '~/services/grid'
import avatarDialog from "~/components/users/AvatarDialog.vue";

export type BuildCell = {
  cell: CellType
  value: ValueType
}

export type BuildMergedCell = {
  cell: CellType
  value: ValueType
  colspan: number
  rowspan: number
  cells: CellType[]
}

export type Cell = BuildCell | BuildMergedCell

export type EditableCell = {
  cell: Cell
  value: ValueType
  newValue: string
}

export type BuildColumn = {
  name: string
  style: Record<string, string>
  dimension: ColumnDimensionType
}

export type BuildRow = {
  name: string
  style: Record<string, string>
  dimension: RowDimensionType
}

export function useGrid (sheet: Ref<SheetType> | SheetType) {
  const grid: Ref<SheetType> = ref<SheetType>(isRef(sheet) ? sheet.value : sheet)

  const columns: ComputedRef = computed(() => (
    grid.value.columns.map((columnDimension: ColumnDimensionType) => ({
      id: columnDimension.id,
      index: columnDimension.index,
      positional: positionToLetter(columnDimension.index),
      style: {
        width: columnDimension.width ? `${columnDimension.width}em` : undefined
      },
      dimension: columnDimension
    }))
  ))

  /**
   * Собираем структуру для быстрого поиска
   */
  const cells: ComputedRef = computed(() => {
    const buildCells = {}
    for (const cell of grid.value.cells) {
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
    for (const value of grid.value.values) {
      if (!(value.rowId in buildValues)) {
        buildValues[value.rowId] = {}
      }
      buildValues[value.rowId][value.columnId] = value
    }
    return buildValues
  })

  const rows: ComputedRef = computed(() => {
    const buildRows = []
    for (let rowIndex = 0; rowIndex < grid.value.rows.length; ++rowIndex) {
      const row = grid.value.rows[rowIndex]
      const buildRow = {
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
      for (let columnIndex = 0; columnIndex < grid.value.columns.length; ++columnIndex) {
        const column: ColumnDimensionType = grid.value.columns[columnIndex]
        const cell: CellType = rowCells[column.id]
        const value: ValueType | null = valueCells && column.id in valueCells ? valueCells[column.id] : null
        const position: string = `${positionToLetter(column.index)}${row.index}`
        // Стили должны формироваться на основе предпочтения cell <- row <- col
        const buildCell = {
          position,
          value: value ? value.value : cell.default,
          editable: cell.editable,
          kind: cell.kind,
          colspan: 1,
          rowspan: 1,
          style: {
            'text-align': cell.horizontalAlign,
            'vertical-align': cell.verticalAlign,
            'font-size': cell.size,
            'font-weight': cell.strong ? 'bold' : 'normal',
            'font-style': cell.italic ? 'italic' : 'normal',
            'text-decoration': cell.underline ? 'underline' : undefined,
            color: cell.color,
            background: cell.background
          },
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
    grid.value.mergedCells.reduce((a, c: MergedCellType) => ({ ...a, [c.target]: c }), {})
  ))

  const mergedCells: ComputedRef<string[]> = computed(() => {
    return Object.values<MergedCellType>(grid.value.mergedCells)
      .reduce<string[]>((a: string[], c: MergedCellType)=> ([...a, ...c.cells]), [])
  })

  /**
   * Блок выделения
   */
  const active: Ref<string | null> = ref<string | null>(null)

  const setActive = (position: string, dbl: boolean = false) => {
    if (active.value === null && dbl) {
      active.value = position
    } else if (active.value !== position) {
      active.value = null
    }
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
