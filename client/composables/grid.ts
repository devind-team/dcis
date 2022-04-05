import { useEventListener } from '@vueuse/core'
import type { ComputedRef, Ref } from '#app'
import { computed, ref, watch, onBeforeUnmount } from '#app'

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
import {
  BuildCellType,
  BuildColumnType,
  ResizingBuildColumnType,
  BuildRowType,
  CellOptionsType
} from '~/types/grid-types'

export const cellKinds: Record<string, string> = {
  n: 'Numeric',
  s: 'String',
  text: 'Text',
  money: 'Money',
  department: 'Department'
}
export const defaultColumnWidth = 64
export const borderGag = 10

export function useGrid (
  sheet: Ref<SheetType>,
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => void
) {
  const columns: ComputedRef<BuildColumnType[]> = computed<BuildColumnType[]>(() => (
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => {
      let width = ''
      if (resizingColumn.value && resizingColumn.value.dimension.id === columnDimension.id) {
        width = `${resizingColumn.value.width}px`
      } else {
        width = columnDimension.width ? `${columnDimension.width}px` : `${defaultColumnWidth}px`
      }
      return {
        id: columnDimension.id,
        index: columnDimension.index,
        position: positionToLetter(columnDimension.index),
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
  const active = ref<string | null>(null)
  const selection = ref<string[]>([])
  const startCellSelectionPosition = ref<string | null>(null)
  /**
   * Начало выделения ячейки по событию MouseDown на ячейке
   */
  const startCellSelection = (position: string): void => {
    startCellSelectionPosition.value = position
  }
  /**
   * Продолжение выделения ячейки по событию MouseMove на ячейке
   */
  const enterCellSelection = (position: string): void => {
    if (startCellSelectionPosition.value) {
      selection.value = rangeLetterToCells(`${startCellSelectionPosition.value}:${position}`)
    }
  }
  /**
   * Завершение выделения ячейки по событию MouseUp на ячейке
   */
  const endCellSelection = (position: string): void => {
    if (startCellSelectionPosition.value) {
      if (position === startCellSelectionPosition.value) {
        setActive(position)
      }
      selection.value = rangeLetterToCells(`${startCellSelectionPosition.value}:${position}`)
      startCellSelectionPosition.value = null
    }
  }
  /**
   * Вычисление выделенных ячеек
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
  const resizingColumn = ref<ResizingBuildColumnType | null>(null)
  const moveColumnHeader = (event: MouseEvent, column: BuildColumnType) => {
    const mousePosition = { x: event.clientX, y: event.clientY }
    const cell = event.target as HTMLTableCellElement
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      resizingColumn.value.width += mousePosition.x - resizingColumn.value.mousePosition.x
      resizingColumn.value.mousePosition = mousePosition
    } else if (cell.offsetWidth - event.offsetX < borderGag) {
      resizingColumn.value = {
        ...column,
        width: column.dimension.width ?? defaultColumnWidth,
        mousePosition,
        state: 'hover'
      }
    } else if (cell.offsetWidth - event.offsetX > cell.offsetWidth - borderGag && column.index - 1 > 0) {
      resizingColumn.value = {
        ...columns.value[column.index - 2],
        width: columns.value[column.index - 2].dimension.width ?? defaultColumnWidth,
        mousePosition,
        state: 'hover'
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
      changeColumnWidth(resizingColumn.value.dimension, resizingColumn.value.width)
      resizingColumn.value.state = 'hover'
    }
  }

  /**
   * Класс курсора на странице
   */
  const cursorClass = computed<'grid__cursor_cell' | 'grid__cursor_col-resize' | null>(() => {
    if (startCellSelectionPosition.value) {
      return 'grid__cursor_cell'
    }
    if (resizingColumn.value) {
      return 'grid__cursor_col-resize'
    }
    return null
  })
  /**
   * Очистка курсора
   */
  const clearCursor = () => {
    document.body.classList.remove('grid__cursor_cell')
    document.body.classList.remove('grid__cursor_col-resize')
  }
  /**
   * Добавляем класс курсора на всю страницу
   */
  watch(cursorClass, (newValue) => {
    if (newValue) {
      document.body.classList.add(newValue)
    } else {
      clearCursor()
    }
  })
  /**
   * Очищаем курсор после перед размонтированием компонента
   */
  onBeforeUnmount(() => {
    clearCursor()
  })

  useEventListener('mouseup', () => {
    if (startCellSelectionPosition.value) {
      startCellSelectionPosition.value = null
    }
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      changeColumnWidth(resizingColumn.value.dimension, resizingColumn.value.width)
      resizingColumn.value = null
    }
  })

  useEventListener('mousemove', (event: MouseEvent) => {
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      const mousePosition = { x: event.clientX, y: event.clientY }
      resizingColumn.value.width += event.x - resizingColumn.value.mousePosition.x
      resizingColumn.value.mousePosition = mousePosition
    }
  })

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
    moveColumnHeader,
    leaveColumnHeader,
    startColumnResizing,
    endColumnResizing
  }
}
