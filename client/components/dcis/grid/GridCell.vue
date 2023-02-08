<template lang="pug">
.grid__cell-content(:class="contentClasses")
  component(
    v-if="renderComponent"
    v-bind="componentProps"
    v-on="componentListeners"
    :is="componentName"
  )
  div(v-else :style="stylesRawValues") {{ formattedCellValue }}
</template>

<script lang="ts">
import { computed, defineComponent, inject, PropType } from '#app'
import numfmt from 'numfmt'
import { useCommonQuery } from '~/composables'
import { useCanChangeValue } from '~/composables/grid-permissions'
import { useChangeValue, useChangeFileValue, useUnloadFileValueArchive } from '~/composables/grid-actions'
import { GridModeInject, ActiveSheetInject, ActiveDocumentInject, GridMode } from '~/types/grid'
import {
  CellType,
  ValueFilesQuery,
  ValueFilesQueryVariables
} from '~/types/graphql'
import { cellKinds } from '~/composables/grid'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'
import GridCellNumeric from '~/components/dcis/grid/cells/GridCellNumeric.vue'
import GridCellString from '~/components/dcis/grid/cells/GridCellString.vue'
import GridCellText from '~/components/dcis/grid/cells/GridCellText.vue'
import GridCellFiles from '~/components/dcis/grid/cells/GridCellFiles.vue'
import GridCellMoney from '~/components/dcis/grid/cells/GridCellMoney.vue'
import GridCellDepartment from '~/components/dcis/grid/cells/GridCellDepartment.vue'
import GridCellClassification from '~/components/dcis/grid/cells/GridCellClassification.vue'

export default defineComponent({
  components: {
    GridCellNumeric,
    GridCellString,
    GridCellText,
    GridCellFiles,
    GridCellMoney,
    GridCellDepartment,
    GridCellClassification
  },
  props: {
    cell: { type: Object as PropType<CellType>, required: true },
    active: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const mode = inject(GridModeInject)
    const activeSheet = inject(ActiveSheetInject)
    const activeDocument = inject(ActiveDocumentInject)

    const cell = computed(() => props.cell)

    const { data: files, update: updateFiles } = useCommonQuery<
      ValueFilesQuery,
      ValueFilesQueryVariables,
      'valueFiles'
    >({
      document: valueFilesQuery,
      variables: {
        documentId: activeDocument.value ? activeDocument.value.id : '',
        sheetId: activeSheet.value.id,
        columnId: props.cell.columnId,
        rowId: props.cell.rowId
      },
      options: computed(() => ({
        enabled: props.active && props.cell.editable && props.cell.kind === 'fl' && mode.value === GridMode.WRITE
      }))
    })

    const canChangeValueFunction = useCanChangeValue()
    const canChangeValue = computed<boolean>(() => canChangeValueFunction(props.cell))

    const changeValue = useChangeValue()
    const changeFileValue = useChangeFileValue(cell, updateFiles)
    const unloadFileValueArchive = useUnloadFileValueArchive(cell)

    const cellKind = computed<string>(() => {
      if (props.cell.kind in cellKinds) {
        if (props.cell.kind === 'fl' && mode.value === GridMode.CHANGE) {
          return 'String'
        }
        return cellKinds[props.cell.kind]
      }
      return 'String'
    })

    const cellValue = computed<string | number | Date | null>(() => {
      if (props.cell.error) {
        return props.cell.error
      }
      if (props.cell.value === null) {
        return props.cell.value
      }
      if (cellKind.value === 'Numeric') {
        return Number(props.cell.value)
      }
      if (cellKind.value === 'Formula') {
        const numberValue = parseFloat(props.cell.value)
        if (isNaN(numberValue)) {
          return props.cell.value
        }
        return numberValue
      }
      if (props.cell.kind === 'd' || props.cell.kind === 'time') {
        return new Date(props.cell.value)
      }
      return props.cell.value
    })
    const formattedCellValue = computed<string>(() => {
      if (props.cell.numberFormat) {
        const fmt = numfmt(props.cell.numberFormat, { locale: 'ru' })
        return fmt(cellValue.value)
      }
      return cellValue.value
    })

    const setValue = async (value: string) => {
      emit('clear-active')
      if (props.cell.value === value || (props.cell.value === null && value === '')) {
        return
      }
      await changeValue(props.cell, value)
    }

    const setFileValue = async (value: string, remainingFiles: string[], newFiles: File[]) => {
      emit('clear-active')
      await changeFileValue(value, remainingFiles, newFiles)
    }

    const uploadArchive = async () => {
      const src = await unloadFileValueArchive()
      window.open(src, '_blank')
    }

    const cancel = () => {
      emit('clear-active')
    }

    const componentName = computed<string>(() => `GridCell${cellKind.value}`)
    const hasFiles = computed<boolean>(() =>
      componentName.value === 'GridCellFiles' && Boolean(files.value) && files.value.length !== 0)
    const renderComponent = computed<boolean>(() =>
      props.active && (hasFiles.value || canChangeValue.value)
    )

    const componentProps = computed(() => {
      if (componentName.value === 'GridCellFiles') {
        return { value: cellValue.value, files: files.value || [], readonly: !canChangeValue.value }
      }
      return { value: cellValue.value, readonly: !canChangeValue.value }
    })

    const componentListeners = computed<Record<string, Function>>(() => {
      if (componentName.value === 'GridCellFiles') {
        return { 'set-value': setFileValue, 'unload-archive': uploadArchive, cancel }
      }
      return { 'set-value': setValue, cancel }
    })

    const contentClasses = computed<Record<string, boolean>>(() => ({
      'grid__cell-content_active': props.active && ['Numeric', 'String', 'Money'].includes(cellKind.value)
    }))

    const stylesRawValues = computed<Record<string, string>>(() => ({
      'white-space': props.cell.kind === 'text' ? 'pre' : undefined
    }))

    return {
      formattedCellValue,
      componentName,
      renderComponent,
      componentProps,
      componentListeners,
      contentClasses,
      stylesRawValues
    }
  }
})
</script>
