import type { ComputedRef, Ref } from '#app'
import { computed, ref } from '#app'

import { useGridMutations } from '~/composables/grid-mutations'
import type { CellType, ColumnDimensionType, MergedCellType, SheetType, ValueType } from '~/types/graphql'

import {
  getCellBorder,
  getCellStyle,
  getCellValue,
  letterToPosition,
  parseCoordinate,
  positionToLetter,
  rangeLetterToCells,
  unionValues
} from '~/services/grid'
import { BuildCellType, BuildColumnType, BuildRowType, CellOptionsType, ColumnResizeType } from '~/types/grid-types'

export const cellKinds: Record<string, string> = {
  n: 'Numeric',
  s: 'String',
  text: 'Text',
  money: 'Money',
  department: 'Department'
}
export const defaultColumnWidth = 64
export const borderGag = 10

export function useGrid (sheet: Ref<SheetType>) {
  const { changeColumnWidth } = useGridMutations()

  const columns: ComputedRef<BuildColumnType[]> = computed<BuildColumnType[]>(() => (
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => {
      let width = ''
      if (resizingColumn.value && resizingColumn.value.column.id === columnDimension.id) {
        width = `${resizingColumn.value.width}px`
      } else {
        width = columnDimension.width ? `${columnDimension.width}px` : `${defaultColumnWidth}px`
      }
      return {
        id: columnDimension.id,
        index: columnDimension.index,
        positional: positionToLetter(columnDimension.index),
        style: { width },
        dimension: columnDimension
      }
    })
  ))

  /**
   * Собираем структуру для быстрого поиска
   */
  const cells = computed<Record<number, Record<number, CellType>>>(() => {
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
  const selection: Ref<string[] | null> = ref<string[]>([])
  let startCellSelectionPosition: string | null = null
  /**
   * Стартуем выделение ячейки по событию MouseDown
   * @param _ - событие нажатия кнопки
   * @param position - начальная позиция
   */
  const startCellSelection = (_: MouseEvent, position: string): void => {
    startCellSelectionPosition = position
  }
  const enterCellSelection = (_: MouseEvent, position: string): void => {
    if (startCellSelectionPosition) {
      selection.value = rangeLetterToCells(`${startCellSelectionPosition}:${position}`)
    }
  }
  const endCellSelection = (_: MouseEvent, position: string): void => {
    if (position === startCellSelectionPosition) {
      setActive(position)
    }
    selection.value = rangeLetterToCells(`${startCellSelectionPosition}:${position}`)
    startCellSelectionPosition = null
  }
  /**
   * Вычислений выделенный ячеек
   */
  const selectionCells: ComputedRef<CellType[]> = computed<CellType[]>(() => (
    selection.value
      .map(parseCoordinate)
      .map(cord => ({ rowId: sheet.value.rows[cord.row - 1].id, columnId: sheet.value.columns[letterToPosition(cord.column) - 1].id }))
      .map(position => (cells.value[position.rowId][position.columnId]))
  ))
  const selectionCellsOptions: ComputedRef<CellOptionsType> = computed<CellOptionsType>(() => {
    const allowOptions: string[] = ['kind', 'horizontalAlign', 'verticalAlign', 'size', 'strong', 'italic', 'underline']
    const aggregateOptions: Record<string, any> = selectionCells.value
      .map((cell: CellType) => Object.fromEntries<string | boolean | null>(
        Object.entries(cell).filter(([k, _]) => allowOptions.includes(k)))
      )
      .reduce(
        (a, c) => {
          for (const k in c) {
            a[k].push(c[k])
          }
          return a
        },
        Object.fromEntries(allowOptions.map(e => ([e, []])))
      )
    return Object.fromEntries(
      Object.entries(aggregateOptions).map(([option, values]) => [option, unionValues(values)])
    ) as CellOptionsType
  })
  const setActive = (position: string) => {
    active.value = position
  }

  /**
   * Блок изменения ширины столбца
   */
  const resizingColumn = ref<ColumnResizeType | null>(null)
  const cursor = computed<string>(() => resizingColumn.value ? 'col-resize' : 'auto')
  const moveColumnHeader = (event: MouseEvent, index: number) => {
    const cell = event.target as HTMLTableCellElement
    const arrayIndex = index - 1
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      resizingColumn.value.width += event.clientX - resizingColumn.value.clientX
      resizingColumn.value.clientX = event.clientX
    } else if (cell.offsetWidth - event.offsetX < borderGag) {
      resizingColumn.value = {
        column: sheet.value.columns[arrayIndex],
        width: sheet.value.columns[arrayIndex].width ?? defaultColumnWidth,
        clientX: event.clientX,
        state: 'hover'
      }
    } else if (cell.offsetWidth - event.offsetX > cell.offsetWidth - borderGag) {
      if (index - 1 > 0) {
        resizingColumn.value = {
          column: sheet.value.columns[arrayIndex - 1],
          width: sheet.value.columns[arrayIndex - 1].width ?? defaultColumnWidth,
          clientX: event.clientX,
          state: 'hover'
        }
      }
    } else {
      resizingColumn.value = null
    }
  }
  const leaveColumnHeader = () => {
    if (resizingColumn.value && resizingColumn.value.state === 'hover') {
      resizingColumn.value = null
    }
  }
  const startColumnResizing = () => {
    if (resizingColumn.value) {
      resizingColumn.value.state = 'resizing'
    }
  }
  const endColumnResizing = () => {
    if (resizingColumn.value) {
      resizingColumn.value.state = 'hover'
      changeColumnWidth(resizingColumn.value.column, resizingColumn.value.width)
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
    selection,
    selectionCells,
    selectionCellsOptions,
    startCellSelection,
    enterCellSelection,
    endCellSelection,
    setActive,
    resizingColumn,
    cursor,
    moveColumnHeader,
    leaveColumnHeader,
    startColumnResizing,
    endColumnResizing
  }
}
