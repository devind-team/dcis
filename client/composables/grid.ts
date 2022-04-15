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
  PositionType,
  BuildCellType,
  BuildColumnType,
  ResizingBuildColumnType,
  ColumnWidthType,
  BuildRowType,
  BoundaryColumnCell,
  BoundaryRowCell,
  CellOptionsType
} from '~/types/grid-types'

export const cellKinds: Record<string, string> = {
  n: 'Numeric',
  s: 'String',
  text: 'Text',
  money: 'Money',
  department: 'Department'
}

export function useGrid (
  sheet: Ref<SheetType>,
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => void
) {
  const rowIndexColumnWidth = ref<number>(30)
  const defaultColumnWidth = ref<number>(64)
  const borderGag = ref<number>(10)

  /**
   * Ширина таблицы
   */
  const gridWidth = computed<number>(
    () => rowIndexColumnWidth.value +
      columns.value.reduce((sum, column) => sum + column.width, 0)
  )

  const columns = computed<BuildColumnType[]>(() => (
    sheet.value.columns.map((columnDimension: ColumnDimensionType) => {
      let width = 0
      if (resizingColumn.value && resizingColumn.value.dimension.id === columnDimension.id) {
        width = resizingColumn.value.width
      } else {
        width = columnDimension.width ? columnDimension.width : defaultColumnWidth.value
      }
      return {
        id: columnDimension.id,
        index: columnDimension.index,
        position: positionToLetter(columnDimension.index),
        width,
        style: { width: `${width}px` },
        dimension: columnDimension
      }
    })
  ))

  /**
   * Собираем структуру для быстрого поиска значений
   */
  const values = computed<Record<number, Record<number, ValueType>>>(() => {
    const buildValues = {}
    for (const value of sheet.value.values) {
      if (!(value.rowId in buildValues)) {
        buildValues[value.rowId] = {}
      }
      buildValues[value.rowId][value.columnId] = value
    }
    return buildValues
  })

  /**
   * Собираем структуру для быстрого поиска объединенных ячеек
   */
  const mergeCells = computed<Record<string, MergedCellType>>(() => (
    sheet.value.mergedCells.reduce((a, c: MergedCellType) => ({ ...a, [c.target]: c }), {})
  ))

  /**
   * Объединенные ячейки
   */
  const mergedCells = computed<string[]>(() => {
    return Object.values<MergedCellType>(sheet.value.mergedCells)
      .reduce<string[]>((a: string[], c: MergedCellType) => ([...a, ...c.cells]), [])
  })

  /**
   * Собираем структуру для быстрого поиска ячеек
   */
  const cells = computed<Record<number, Record<number, BuildCellType>>>(() => {
    const buildCells = {}
    for (const cell of sheet.value.cells) {
      if (!(cell.rowId in buildCells)) {
        buildCells[cell.rowId] = {}
      }
      const row = sheet.value.rows.find(row => row.id === String(cell.rowId))
      const column = sheet.value.columns.find(column => column.id === String(cell.columnId))
      const position = `${positionToLetter(column.index)}${row.index}`
      const valueCells: Record<number, ValueType> | null = row.id in values.value ? values.value[row.id] : null
      const buildCell: BuildCellType = {
        sheetId: sheet.value.id,
        id: cell.id,
        position,
        value: getCellValue(valueCells && column.id in valueCells ? valueCells[column.id] : null, cell),
        editable: cell.editable,
        kind: cell.kind,
        colspan: 1,
        rowspan: 1,
        style: getCellStyle(cell),
        border: getCellBorder(cell),
        column,
        row,
        cell
      }
      if (position in mergeCells.value) {
        Object.assign(buildCell, mergeCells.value[position])
      }
      buildCells[cell.rowId][cell.columnId] = buildCell
    }
    return buildCells
  })

  const rows = computed<BuildRowType[]>(() => {
    const buildRows: BuildRowType[] = []
    for (const row of sheet.value.rows) {
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
      const rowCells: Record<number, CellType> = cells.value[row.id]
      for (const column of sheet.value.columns) {
        const buildCell: BuildCellType = rowCells[column.id]
        const position = `${positionToLetter(column.index)}${row.index}`
        if (position in mergeCells.value || !mergedCells.value.includes(position)) {
          buildRow.cells.push(buildCell)
        }
      }
      buildRows.push(buildRow)
    }
    return buildRows
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
  const selectionCells = computed<BuildCellType[]>(() => (
    selection.value
      .map(parseCoordinate)
      .map(cord => ({
        rowId: sheet.value.rows[cord.row - 1].id,
        columnId: sheet.value.columns[letterToPosition(cord.column) - 1].id
      }))
      .map(position => (cells.value[position.rowId][position.columnId]))
  ))
  /**
   * Вычисление выделенных столбцов
   */
  const selectionColumns = computed<number[]>(() =>
    [...new Set(selectionCells.value.reduce((acc, cell) => {
      const columns: number[] =
        Array.from({ length: cell.colspan }).map((_, index) => cell.column.index + index)
      return [...acc, ...columns]
    }, []))]
  )
  /**
   * Вычисление выделенных строк
   */
  const selectionRows = computed<number[]>(() =>
    [...new Set(selectionCells.value.reduce((acc, cell) => {
      const rows: number[] =
        Array.from({ length: cell.rowspan }).map((_, index) => cell.row.index + index)
      return [...acc, ...rows]
    }, []))]
  )
  /**
   * Вычисление ячеек граничных к крайнему фиксированному столбцу
   */
  const boundaryColumnCells = computed<BoundaryColumnCell[]>(() => {
    const result: BoundaryColumnCell[] = []
    let i = 0
    while (i < rows.value.length) {
      const cell = rows.value[i].cells[0]
      result.push({ cell, rows: rows.value.slice(i, i + cell.rowspan) })
      i += cell.rowspan
    }
    return result
  })
  /**
   * Вычисление выделенных ячеек граничных к крайнему фиксированному столбцу
   */
  const selectedBoundaryColumnCells = computed<BoundaryColumnCell[]>(() =>
    boundaryColumnCells.value.filter(boundaryCell => selection.value.includes(boundaryCell.cell.position))
  )
  /**
   * Вычисление ячеек граничных к крайней фиксированной строке
   */
  const boundaryRowCells = computed<BoundaryRowCell[]>(() => {
    const result: BoundaryRowCell[] = []
    let i = 0
    while (i < columns.value.length) {
      const cell = rows.value[0].cells[i]
      result.push({ cell, columns: columns.value.slice(i, i + cell.colspan) })
      i += cell.colspan
    }
    return result
  })
  /**
   * Вычисление выделенных ячеек граничных к крайней фиксированной строке
   */
  const selectedBoundaryRowCells = computed<BoundaryRowCell[]>(() =>
    boundaryRowCells.value.filter(boundaryCell => selection.value.includes(boundaryCell.cell.position))
  )
  const selectionCellsOptions: ComputedRef<CellOptionsType> = computed<CellOptionsType>(() => {
    const allowOptions: string[] = ['kind', 'horizontalAlign', 'verticalAlign', 'size', 'strong', 'italic', 'underline']
    const aggregateOptions: Record<string, any> = selectionCells.value
      .map((buildCell: BuildCellType) => Object.fromEntries<string | boolean | null>(
        Object.entries(buildCell.cell).filter(([k, _]) => allowOptions.includes(k)))
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
  const gridContainer = ref<HTMLDivElement | null>(null)
  const resizingColumn = ref<ResizingBuildColumnType | null>(null)
  const columnWidthPosition = ref<PositionType>({ left: null, right: null, top: null, bottom: null })
  const columnWidth = computed<ColumnWidthType>(() => ({
    visible: !!resizingColumn.value && resizingColumn.value.state === 'resizing',
    position: columnWidthPosition.value,
    width: resizingColumn.value?.width ?? 0
  }))
  const moveColumnHeader = (event: MouseEvent, column: BuildColumnType) => {
    const mousePosition = { x: event.clientX, y: event.clientY }
    const cell = event.target as HTMLTableCellElement
    if (resizingColumn.value && resizingColumn.value.state === 'resizing') {
      resizingColumn.value.width = Math.max(
        resizingColumn.value.width + mousePosition.x - resizingColumn.value.mousePosition.x, 0
      )
      resizingColumn.value.mousePosition = mousePosition
    } else if (cell.offsetWidth - event.offsetX < borderGag.value) {
      resizingColumn.value = {
        ...column,
        width: column.dimension.width ?? defaultColumnWidth.value,
        mousePosition,
        state: 'hover'
      }
    } else if (cell.offsetWidth - event.offsetX > cell.offsetWidth - borderGag.value && column.index - 1 > 0) {
      resizingColumn.value = {
        ...columns.value[column.index - 2],
        width: columns.value[column.index - 2].dimension.width ?? defaultColumnWidth.value,
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
  const startColumnResizing = (event: MouseEvent) => {
    if (resizingColumn.value) {
      const cell = event.target as HTMLTableCellElement
      if (cell.offsetLeft - gridContainer.value.scrollLeft + event.offsetX < document.body.offsetWidth - 150) {
        columnWidthPosition.value = {
          left: cell.offsetLeft - gridContainer.value.scrollLeft + event.offsetX,
          right: null,
          top: cell.offsetTop + event.offsetY - 25,
          bottom: null
        }
      } else {
        columnWidthPosition.value = {
          left: null,
          right: 25,
          top: cell.offsetTop + event.offsetY - 25,
          bottom: null
        }
      }
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
   * Очищаем курсор перед размонтированием компонента
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
      resizingColumn.value.width = Math.max(
        resizingColumn.value.width + mousePosition.x - resizingColumn.value.mousePosition.x, 0
      )
      resizingColumn.value.mousePosition = mousePosition
    }
  })

  return {
    rowIndexColumnWidth,
    defaultColumnWidth,
    borderGag,
    sheet,
    gridWidth,
    cells,
    columns,
    rows,
    values,
    mergeCells,
    mergedCells,
    active,
    selection,
    selectionCells,
    selectionColumns,
    selectionRows,
    boundaryColumnCells,
    selectedBoundaryColumnCells,
    boundaryRowCells,
    selectedBoundaryRowCells,
    selectionCellsOptions,
    startCellSelection,
    enterCellSelection,
    endCellSelection,
    setActive,
    gridContainer,
    columnWidth,
    moveColumnHeader,
    leaveColumnHeader,
    startColumnResizing,
    endColumnResizing
  }
}
