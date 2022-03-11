import { useMutation } from '@vue/apollo-composable'
import { computed, ref } from '#app'
import type { ComputedRef, Ref } from '#app'
import type {
  SheetType,
  ColumnDimensionType,
  RowDimensionType,
  CellType,
  ValueType,
  ChangeValueMutation,
  ChangeValueMutationVariables
} from '~/types/graphql'
import { positionToLetter } from '~/services/grid'
import changeValueMutation from '~/gql/dcis/mutations/document/change_value.graphql'

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
  cells: Cell[]
}

export function useGrid (sheet: ComputedRef<SheetType | null>) {
  const { mutate: changeValueMutate } = useMutation<ChangeValueMutation, ChangeValueMutationVariables>(
    changeValueMutation
  )

  const getValue = (cell: CellType): ValueType => sheet.value.values
    .find(value => value.row.id === cell.row.id && value.column.id === cell.column.id)!

  const mergedCells: ComputedRef<BuildMergedCell[]> = computed<BuildMergedCell[]>(() => sheet.value
    ? sheet.value.mergedCells.map((mergedCell) => {
      const cells: CellType[] = []
      for (let column = mergedCell.minCol; column <= mergedCell.maxCol; column++) {
        for (let row = mergedCell.minRow; row <= mergedCell.maxRow; row++) {
          cells.push(
            sheet.value.cells.find(cell => column === cell.column.index + 1 && row === cell.row.index + 1)!
          )
        }
      }
      const cell = cells[0]
      return {
        cell,
        value: getValue(cell),
        colspan: mergedCell.maxCol - mergedCell.minCol + 1,
        rowspan: mergedCell.maxRow - mergedCell.minRow + 1,
        cells
      }
    })
    : []
  )

  const findCell = (
    rowDimension: RowDimensionType,
    columnDimension: ColumnDimensionType
  ): Cell | null => {
    for (const mergedCell of mergedCells.value) {
      if (mergedCell.cell.row.id === rowDimension.id && mergedCell.cell.column.id === columnDimension.id) {
        return mergedCell
      }
      if (mergedCell.cells.find(cell => cell.row.id === rowDimension.id && cell.column.id === columnDimension.id)) {
        return null
      }
    }
    const cell = sheet.value.cells
      .find(cell => cell.row.id === rowDimension.id && cell.column.id === columnDimension.id)!
    return {
      cell,
      value: getValue(cell)
    }
  }

  const columns: ComputedRef<BuildColumn[]> = computed<BuildColumn[]>(() => sheet.value
    ? sheet.value.columns.map(columnDimension => ({
      name: positionToLetter(columnDimension.index + 1),
      style: {
        width: `${columnDimension.width}px`
      },
      dimension: columnDimension
    }))
    : []
  )
  const rows: ComputedRef<BuildRow[]> = computed<BuildRow[]>(() => sheet.value
    ? sheet.value.rows.map(rowDimension => ({
      name: String(rowDimension.index + 1),
      style: {
        height: `${rowDimension.height}px`
      },
      dimension: rowDimension,
      cells: sheet.value.columns.map(columnDimension => findCell(rowDimension, columnDimension)).filter(cell => cell)
    }))
    : []
  )

  const activeCell: Ref<Cell | null> = ref<Cell | null>(null)
  const editableCell: Ref<EditableCell | null> = ref<EditableCell | null>(null)

  const isActive = (cell: Cell): boolean => {
    return activeCell.value && activeCell.value.cell.id === cell.cell.id
  }

  const isEditable = (cell: Cell): boolean => {
    return editableCell.value && editableCell.value.cell.cell.id === cell.cell.id
  }

  const isCurrent = (cell: Cell): boolean => {
    return isActive(cell) || isEditable(cell)
  }

  const changeCellValue = async (editableCell: EditableCell): Promise<void> => {
    await changeValueMutate({
      valueId: editableCell.value.id,
      value: editableCell.newValue
    })
  }

  const activateCell = async (cell: Cell): Promise<void> => {
    if (isCurrent(cell)) {
      return
    }
    if (editableCell.value) {
      await changeCellValue(editableCell.value)
    }
    activeCell.value = cell
    editableCell.value = null
  }

  const editCell = async (cell: Cell): Promise<void> => {
    if (isEditable(cell)) {
      return
    }
    if (editableCell.value) {
      await changeCellValue(editableCell.value)
    }
    activeCell.value = cell
    const value = getValue(cell.cell)
    editableCell.value = {
      cell,
      value,
      newValue: value.value
    }
  }

  return { columns, rows, activeCell, editableCell, isActive, isEditable, isCurrent, activateCell, editCell }
}
