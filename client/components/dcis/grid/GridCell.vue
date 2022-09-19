<template lang="pug">
.grid__cell-content(:class="contentClasses")
  component(
    v-if="renderComponent"
    v-bind="componentProps"
    v-on="componentListeners"
    :is="componentName"
  )
  div(v-else style="white-space: pre") {{ formattedCellValue }}
</template>

<script lang="ts">
import { computed, defineComponent, inject, PropType, Ref } from '#app'
import { useApolloClient } from '@vue/apollo-composable'
import {
  UpdateType,
  useChangeCellDefaultMutation,
  useChangeFileValueMutation,
  useChangeValueMutation,
  useCommonQuery,
  useUnloadFileValueArchiveMutation
} from '~/composables'
import { useAuthStore } from '~/stores'
import { GridMode, UpdateSheetType } from '~/types/grid'
import {
  CellType,
  DivisionModelType,
  DocumentSheetQuery,
  DocumentsSheetQuery,
  DocumentType,
  SheetType,
  ValueFilesQuery,
  ValueFilesQueryVariables
} from '~/types/graphql'
import { cellKinds } from '~/composables/grid'
import GridCellNumeric from '~/components/dcis/grid/cells/GridCellNumeric.vue'
import GridCellString from '~/components/dcis/grid/cells/GridCellString.vue'
import GridCellText from '~/components/dcis/grid/cells/GridCellText.vue'
import GridCellFiles from '~/components/dcis/grid/cells/GridCellFiles.vue'
import GridCellMoney from '~/components/dcis/grid/cells/GridCellMoney.vue'
import GridCellDepartment from '~/components/dcis/grid/cells/GridCellDepartment.vue'
import GridCellClassification from '~/components/dcis/grid/cells/GridCellClassification.vue'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'

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
    const { client } = useApolloClient()

    const userStore = useAuthStore()

    const mode = inject<GridMode>('mode')
    const activeDocument = inject<Ref<DocumentType | null>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateSheetType>>('updateActiveSheet')

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
        enabled: props.active && props.cell.editable && props.cell.kind === 'fl' && mode === GridMode.WRITE
      }))
    })

    const changeDefault = mode === GridMode.CHANGE
      ? useChangeCellDefaultMutation(updateSheet as Ref<UpdateType<DocumentsSheetQuery>>)
      : null
    const changeValue = mode === GridMode.WRITE
      ? useChangeValueMutation(
        computed(() => activeDocument.value.id),
        computed(() => activeSheet.value.id),
        computed(() => props.cell),
        client
      )
      : null

    const changeFileValue = mode === GridMode.WRITE
      ? useChangeFileValueMutation(
        computed(() => activeDocument.value.id),
        computed(() => activeSheet.value.id),
        computed(() => props.cell),
        updateSheet as Ref<UpdateType<DocumentSheetQuery>>,
        updateFiles
      )
      : null

    const unloadFileValueArchive = mode === GridMode.WRITE
      ? useUnloadFileValueArchiveMutation(
        computed(() => activeDocument.value ? activeDocument.value.id : ''),
        computed(() => activeSheet.value.id),
        computed(() => props.cell)
      )
      : null

    const cellKind = computed<string>(() => {
      if (props.cell.kind in cellKinds) {
        if (props.cell.kind === 'fl' && mode === GridMode.CHANGE) {
          return 'String'
        }
        return cellKinds[props.cell.kind]
      }
      return 'String'
    })

    const cellValue = computed<string | number | null>(() => {
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
      return props.cell.value
    })
    const formattedCellValue = computed<string>(() => {
      if (typeof cellValue.value === 'number') {
        return new Intl.NumberFormat('ru-RU', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        }).format(cellValue.value)
      }
      return cellValue.value
    })

    const setValue = async (value: string) => {
      emit('clear-active')
      if (props.cell.value === value || (props.cell.value === null && value === '')) {
        return
      }
      mode === GridMode.CHANGE ? await changeDefault(props.cell, value) : await changeValue(value)
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

    const canChangeValue = computed<boolean>(() => {
      if (mode === GridMode.CHANGE) {
        return true
      }
      if (!activeDocument.value.lastStatus.status.edit || !props.cell.editable || props.cell.kind === 'f') {
        return false
      }
      if (
        activeSheet.value.canChange ||
        activeSheet.value.canChangeValue ||
        activeDocument.value.user?.id === userStore.user.id
      ) {
        return true
      }
      const userDivisionIds = userStore.user.divisions.map((division: DivisionModelType) => division.id)
      if (activeDocument.value.period.multiple) {
        return userDivisionIds.includes(activeDocument.value.objectId)
      }
      return userDivisionIds.includes(props.cell.rowId)
    })

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

    return { formattedCellValue, componentName, renderComponent, componentProps, componentListeners, contentClasses }
  }
})
</script>
