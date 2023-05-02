<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-snackbar(v-model="successUpload" right) {{ $t('dcis.grid.sheetMenu.scanMenu.snackbars.scanIsLoaded') }}
      template(#action="{ attrs: snackbarAttrs }")
        v-btn(v-bind="{ snackbarAttrs }" icon @click="successUpload = false")
          v-icon mdi-close
    v-snackbar(v-model="successDelete" right) {{ $t('dcis.grid.sheetMenu.scanMenu.snackbars.scanIsDeleted') }}
      template(#action="{ attrs: snackbarAttrs }")
        v-btn(v-bind="{ snackbarAttrs }" icon @click="successDelete = false")
          v-icon mdi-close
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.scanMenu.buttonText') }}
  v-list(dense width="200")
    v-list-item(v-if="!document.scan" @click="open")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.scanMenu.uploadScan') }}
    v-list-item(v-if="document.scan" :href="`/${document.scan.src}`" target="__blank")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.scanMenu.downloadScan') }}
    v-list-item(v-if="document.scan" @click="deleteDocumentScanMutate({ fileId: document.scan.id }).then()")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.scanMenu.deleteScan') }}
</template>

<script lang="ts">
import { ref, watch, defineComponent, PropType } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { useFileDialog } from '@vueuse/core'
import {
  DeleteDocumentScanMutation,
  DeleteDocumentScanMutationVariables,
  DocumentQuery,
  DocumentScanFieldsFragment,
  DocumentType,
  UploadDocumentScanMutation,
  UploadDocumentScanMutationVariables
} from '~/types/graphql'
import uploadDocumentScan from '~/gql/dcis/mutations/document/upload_document_scan.graphql'
import deleteDocumentScan from '~/gql/dcis/mutations/document/delete_document_scan.graphql'
import { UpdateType } from '~/composables'

export default defineComponent({
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    update: { type: Function as PropType<UpdateType>, required: true }
  },
  setup (props) {
    const successUpload = ref<boolean>(false)
    const successDelete = ref<boolean>(false)

    const {
      mutate: uploadDocumentScanMutate,
      onDone: uploadDocumentScanOnDone
    } = useMutation<
      UploadDocumentScanMutation,
      UploadDocumentScanMutationVariables
    >(
      uploadDocumentScan,
      {
        update: (cache, result) => {
          if (result.data.uploadDocumentScan.success) {
            props.update(
              cache,
              result,
              (data: DocumentQuery, result) => {
                data.document.scan = result.data.uploadDocumentScan.documentScan as DocumentScanFieldsFragment
                return data
              }
            )
          }
        }
      }
    )
    uploadDocumentScanOnDone((result) => {
      successUpload.value = result.data.uploadDocumentScan.success
    })

    const { files, open } = useFileDialog({ multiple: false, accept: 'application/pdf' })
    watch(files, (files: FileList) => {
      uploadDocumentScanMutate({ documentId: props.document.id, scanFile: files[0] })
    })

    const {
      mutate: deleteDocumentScanMutate,
      onDone: deleteDocumentScanOnDone
    } = useMutation<
      DeleteDocumentScanMutation,
      DeleteDocumentScanMutationVariables
    >(
      deleteDocumentScan,
      {
        update: (cache, result) => {
          if (result.data.deleteDocumentScan.success) {
            props.update(
              cache,
              result,
              (data: DocumentQuery) => {
                data.document.scan = null
                return data
              }
            )
          }
        }
      }
    )
    deleteDocumentScanOnDone(
      (result) => {
        successDelete.value = result.data.deleteDocumentScan.success
      }
    )

    return { open, successUpload, successDelete, deleteDocumentScanMutate }
  }
})
</script>
