<template lang="pug">
v-menu(offset-y)
  template(#activator="{ on, attrs }")
    v-snackbar(v-model="successActive" right ) {{ 'Файл загружен' }}
      template(#action="{ attrs: snackbarAttrs }")
        v-btn(v-bind="{ snackbarAttrs }" icon @click="successActive = false")
          v-icon mdi-close
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.scanMenu.buttonText') }}
  v-list(dense width="200")
    v-list-item(@click="open")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.scanMenu.uploadScan') }}
    v-list-item(v-if="document.scan" :href="`/${document.scan.src}`" target="__blank")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.scanMenu.downloadScan') }}
    v-list-item(v-if="document.scan" @click="deleteDocumentScanMutate({ fileId: document.scan.id }).then()")
      v-list-item-title {{ $t('dcis.grid.sheetMenu.scanMenu.deleteScan') }}
</template>

<script lang="ts">
import { ref, watch, defineComponent, PropType } from '#app'
import { useApolloClient, useMutation } from '@vue/apollo-composable'
import { useFileDialog } from '@vueuse/core'
import { useCommonQuery } from '~/composables'
import {
  DeleteDocumentScanMutation,
  DeleteDocumentScanMutationVariables,
  DocumentScanQuery,
  DocumentScanQueryVariables,
  DocumentType,
  UploadDocumentScanMutation,
  UploadDocumentScanMutationVariables
} from '~/types/graphql'
import documentScanQuery from '~/gql/dcis/queries/document_scan.graphql'
import uploadDocumentScan from '~/gql/dcis/mutations/document/upload_document_scan.graphql'
import deleteDocumentScan from '~/gql/dcis/mutations/document/delete_document_scan.graphql'

export default defineComponent({
  props: {
    document: { type: Object as PropType<DocumentType>, required: true }
  },
  setup (props) {
    const {
      mutate: uploadDocumentScanMutate,
      onDone: uploadDocumentScanOnDone
    } = useMutation<UploadDocumentScanMutation, UploadDocumentScanMutationVariables>(uploadDocumentScan)
    uploadDocumentScanOnDone((result) => {
      successActive.value = result.data.uploadDocumentScan.success
    })

    const successActive = ref<boolean>(false)
    const { files, open } = useFileDialog({ multiple: false, accept: 'application/pdf' })
    watch(files, (files: FileList) => {
      uploadDocumentScanMutate({ documentId: props.document.id, scanFile: files[0] })
    })
    const { mutate: deleteDocumentScanMutate } = useMutation<DeleteDocumentScanMutation, DeleteDocumentScanMutationVariables>(deleteDocumentScan)

    return { open, successActive, deleteDocumentScanMutate }
  }
})
</script>
