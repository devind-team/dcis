import { useEventListener } from '@vueuse/core'
import type { ComputedRef, Ref } from '#app'
import { computed, ref, watch, onBeforeUnmount } from '#app'

import type { ColumnDimensionType, SheetType } from '~/types/graphql'

import {
  parseCoordinate,
  rangeLetterToCells,
  unionValues
} from '~/services/old-grid'
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
  fl: 'Files',
  money: 'Money',
  department: 'Department',
  classification: 'Classification'
}

export function useOldGrid (
  sheet: Ref<SheetType>,
  changeColumnWidth: (columnDimension: ColumnDimensionType, width: number) => void
) {
  const rowIndexColumnWidth = ref<number>(30)
  const borderGag = ref<number>(10)

  /**
   * Ширина таблицы
   */
  const gridWidth = computed<number>(
    () => rowIndexColumnWidth.value +
      columns.value.reduce((sum, column) => sum + column.width, 0)
  )

  /**
   * Блок выделения
   */
  const active = ref<string | null>(null)
  const selectionRange = ref<string | null>(null)
  const selection = computed<string[]>(() => selectionRange.value ? rangeLetterToCells(selectionRange.value) : [])
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
      selectionRange.value = `${startCellSelectionPosition.value}:${position}`
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
      selectionRange.value = `${startCellSelectionPosition.value}:${position}`
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
   * Выделены ли все ячейки
   */
  const allSelected = computed<boolean>(() => selectionRange.value ===
    `A1:${columns.value.at(-1).position}${rows.value.at(-1).index}`
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
    let offset = 0
    while (i < columns.value.length) {
      const cell = rows.value[0].cells[i - offset]
      result.push({ cell, columns: columns.value.slice(i, i + cell.colspan) })
      offset += cell.colspan - 1
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
   * Блок изменения ширины столбца и массового выделения
   */
  const gridContainer = ref<HTMLDivElement | null>(null)
  const resizingColumn = ref<ResizingBuildColumnType | null>(null)
  const columnWidthPosition = ref<PositionType>({ left: null, right: null, top: null, bottom: null })
  const columnWidth = computed<ColumnWidthType>(() => ({
    visible: !!resizingColumn.value && resizingColumn.value.state === 'resizing',
    position: columnWidthPosition.value,
    width: resizingColumn.value?.width ?? 0
  }))

  const startColumnSelectionPosition = ref<string | null>(null)
  const startRowSelectionPosition = ref<number | null>(null)

  const mouseenterColumnIndex = (column: BuildColumnType) => {
    if (startColumnSelectionPosition.value) {
      selectionRange.value = `${startColumnSelectionPosition.value}1:${column.position}${rows.value.at(-1).index}`
    }
  }
  const mousemoveColumnIndex = (event: MouseEvent, column: BuildColumnType) => {
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
  const mouseleaveColumnIndex = () => {
    if (resizingColumn.value && resizingColumn.value.state === 'hover') {
      resizingColumn.value = null
    }
  }
  const mousedownColumnIndex = (event: MouseEvent, column: BuildColumnType) => {
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
    } else {
      startColumnSelectionPosition.value = column.position
      selectionRange.value = `${column.position}1:${column.position}${rows.value.at(-1).index}`
    }
  }
  const mouseupColumnIndex = () => {
    if (resizingColumn.value) {
      changeColumnWidth(resizingColumn.value.dimension, resizingColumn.value.width)
      resizingColumn.value.state = 'hover'
    }
  }
  const mouseenterRowIndex = (row: BuildRowType) => {
    if (startRowSelectionPosition.value) {
      selectionRange.value = `A${startRowSelectionPosition.value}:${columns.value.at(-1).position}${row.index}`
    }
  }
  const mousedownRowIndex = (row: BuildRowType) => {
    startRowSelectionPosition.value = row.index
    selectionRange.value = `A${row.index}:${columns.value.at(-1).position}${row.index}`
  }
  const selectAll = () => {
    selectionRange.value = `A1:${columns.value.at(-1).position}${rows.value.at(-1).index}`
  }

  /**
   * Класс курсора на странице
   */
  const cursorClass = computed<'grid__cursor_cell' | 'grid__cursor_col-resize' | null>(() => {
    if (startCellSelectionPosition.value || startColumnSelectionPosition.value || startRowSelectionPosition.value) {
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
    if (startColumnSelectionPosition.value) {
      startColumnSelectionPosition.value = null
    }
    if (startRowSelectionPosition.value) {
      startRowSelectionPosition.value = null
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
    active,
    selectionRange,
    selection,
    selectionCells,
    selectionColumns,
    selectionRows,
    allSelected,
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
    mouseenterColumnIndex,
    mousemoveColumnIndex,
    mouseleaveColumnIndex,
    mousedownColumnIndex,
    mouseupColumnIndex,
    mouseenterRowIndex,
    mousedownRowIndex,
    selectAll
  }
}
