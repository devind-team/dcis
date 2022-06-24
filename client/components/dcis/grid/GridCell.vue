<template lang="pug">
  .grid__cell-content(:class="contentClasses")
    component(
      v-if="active && cell.editable && !cell.formula"
      v-bind="cellProps"
      v-on="cellListeners"
      :is="`GridCell${cellKind}`"
    )
    template(v-else) {{ cell.value }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, Ref } from '#app'
import {
  UpdateType,
  useChangeFileValueMutation,
  useChangeValueMutation,
  useUnloadFileValueArchiveMutation
} from '~/composables'
import {
  DocumentType,
  SheetQuery,
  SheetType,
  CellType,
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
    const activeDocument = inject<Ref<DocumentType>>('activeDocument')
    const activeSheet = inject<Ref<SheetType>>('activeSheet')
    const updateSheet = inject<Ref<UpdateType<SheetQuery>>>('updateActiveSheet')

    const { data: files, update: updateFiles } = useCommonQuery<
      ValueFilesQuery,
      ValueFilesQueryVariables,
      'valueFiles'
    >({
      document: valueFilesQuery,
      variables: {
        documentId: activeDocument.value.id,
        sheetId: activeSheet.value.id,
        columnId: props.cell.columnId,
        rowId: props.cell.rowId
      },
      options: computed(() => ({
        enabled: props.active && props.cell.editable && props.cell.kind === 'fl'
      }))
    })

    const changeValue = useChangeValueMutation(
      computed(() => activeDocument.value.id),
      computed(() => activeSheet.value.id),
      computed(() => props.cell),
      updateSheet
    )

    const changeFileValue = useChangeFileValueMutation(
      computed(() => activeDocument.value.id),
      computed(() => activeSheet.value.id),
      computed(() => props.cell),
      updateSheet,
      updateFiles
    )

    const unloadFileValueArchive = useUnloadFileValueArchiveMutation(
      computed(() => activeDocument.value.id),
      computed(() => activeSheet.value.id),
      computed(() => props.cell)
    )

    const setValue = async (value: string) => {
      emit('clear-active')
      if (props.cell.value !== value) {
        await changeValue(value)
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

    const cellProps = computed<object>(() => {
      if (props.cell.kind === 'fl') {
        return { value: props.cell.value, files: files.value || [] }
      }
      return { value: props.cell.value }
    })

    const cellListeners = computed<Record<string, Function>>(() => {
      if (props.cell.kind === 'fl') {
        return { 'set-value': setFileValue, 'unload-archive': uploadArchive, cancel }
      }
      return { 'set-value': setValue, cancel }
    })

    const cellKind = computed<string>(() => (
      props.cell.kind in cellKinds ? cellKinds[props.cell.kind] : 'String'
    ))

    const contentClasses = computed<Record<string, boolean>>(() => ({
      'grid__cell-content_active': props.active && ['n', 's', 'money'].includes(props.cell.kind)
    }))

    return { cellKind, contentClasses, cellProps, cellListeners }
  }
})
</script>
