import { computed } from '#app'
import type { ComputedRef } from '#app'
import type { SheetType, ColumnDimensionType, RowDimensionType, CellType, ValueType } from '~/types/graphql'
import { positionToLetter } from '~/services/grid'

export type BuildCell = {
  value: ValueType
  cell: CellType
  colspan?: number
  rowspan?: number
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
  cells: BuildCell[]
}

export function useGrid (sheet: ComputedRef<SheetType | null>) {
  const columns: ComputedRef<BuildColumn[]> = computed<BuildColumn[]>(
    () => sheet.value
      ? sheet.value.columns.map(columnDimension => ({
        name: positionToLetter(columnDimension.index + 1),
        style: {
          width: `${columnDimension.width}px`
        },
        dimension: columnDimension
      }))
      : []
  )
  const rows: ComputedRef<BuildRow[]> = computed<BuildRow[]>(
    () => sheet.value
      ? sheet.value.rows.map(rowDimension => ({
        name: String(rowDimension.index + 1),
        style: {
          height: `${rowDimension.height}px`
        },
        dimension: rowDimension,
        cells: sheet.value.cells
          .filter(cell => cell.row.id === rowDimension.id)
          .map((cell) => {
            const value = sheet.value.values
              .filter(value => value.row.id === cell.row.id && value.column.id === cell.column.id)[0]
            return {
              cell,
              value
            }
          })
      }))
      : []
  )
  return { columns, rows }
}
