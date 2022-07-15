<template lang="pug">
.grid__cell-content(:class="contentClasses")
  component(
    v-if="active && cell.canChangeValue"
    v-bind="cellProps"
    v-on="cellListeners"
    :is="`GridCell${cellKind}`"
  )
  template(v-else) {{ cell.value }}
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
import { GridMode, UpdateSheetType } from '~/types/grid'
import {
  CellType,
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

    const setValue = async (value: string) => {
      emit('clear-active')
      if (props.cell.value !== value) {
        if (mode === GridMode.CHANGE) {
          await changeDefault(props.cell, value)
        } else {
          await changeValue(value)
        }
      }
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

    const cellKind = computed<string>(() => {
      if (props.cell.kind in cellKinds) {
        if (props.cell.kind === 'fl' && mode === GridMode.CHANGE) {
          return 'String'
        }
        return cellKinds[props.cell.kind]
      }
      return 'String'
    })

    const cellProps = computed<object>(() => {
      if (props.cell.kind === 'fl') {
        return { value: props.cell.value, files: files.value || [] }
      }
      return { value: props.cell.value }
    })

    const cellListeners = computed<Record<string, Function>>(() => {
      if (cellKind.value === 'Files') {
        return { 'set-value': setFileValue, 'unload-archive': uploadArchive, cancel }
      }
      return { 'set-value': setValue, cancel }
    })

    const contentClasses = computed<Record<string, boolean>>(() => ({
      'grid__cell-content_active': props.active && ['Numeric', 'String', 'Money'].includes(cellKind.value)
    }))

    return { cellKind, cellProps, cellListeners, contentClasses }
  }
})
</script>
