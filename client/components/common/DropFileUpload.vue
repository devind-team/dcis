<template lang="pug">
v-sheet(height="200" style="cursor:pointer; border:dashed; border-color: gray;")
  v-container(fill-height)
    v-row(justify="center")
      v-icon(v-show="!dragover && !error" size="70") mdi-cloud-upload-outline
      v-icon(v-show="dragover && !error" size="70") mdi-arrow-collapse-down
      v-icon(v-show="error" size="70") mdi-minus-circle
    v-row(justify="center")
      span {{$t('common.dropFileUpload.dropOrClick')}}
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from 'vue-property-decorator'

@Component<DropFileUpload>({})
export default class DropFileUpload extends Vue {
  @Prop() type!: string // text, image, video, application
  dragover: boolean = false
  error: boolean = false
  fileInput: HTMLInputElement | null = null

  mounted () {
    const fileInput = document.createElement('input')
    fileInput.type = 'file'
    fileInput.multiple = true
    fileInput.accept = `${this.type}/*`
    fileInput.onchange = () => {
      this.filesSelected(fileInput.files!)
    }
    this.fileInput = fileInput
    const dropZone = this.$el
    dropZone.addEventListener('dragenter', this.onDragEnter)
    dropZone.addEventListener('dragleave', this.onDragLeave)
    dropZone.addEventListener('dragover', this.onDragOver)
    dropZone.addEventListener('drop', this.onDrop)
    dropZone.addEventListener('click', this.onClick)
    dropZone.addEventListener('keypress', this.onKeyPress)
  }

  beforeDestroy () {
    const dropZone = this.$el
    dropZone.removeEventListener('dragenter', this.onDragEnter)
    dropZone.removeEventListener('dragleave', this.onDragLeave)
    dropZone.removeEventListener('dragover', this.onDragOver)
    dropZone.removeEventListener('drop', this.onDrop)
    dropZone.removeEventListener('click', this.onClick)
    dropZone.removeEventListener('keypress', this.onKeyPress)
  }

  onDragEnter (e:Event) {
    e.preventDefault()
    const t = e as DragEvent
    if (t.dataTransfer?.types && this.isTypesValid(t.dataTransfer.items)) {
      this.dragover = true
    } else {
      this.error = true
    }
  }

  onDragLeave (e:Event) {
    e.preventDefault()
    this.dragover = false
    this.error = false
  }

  onDragOver (e:Event) {
    e.preventDefault()
    const t = e as DragEvent
    if (t.dataTransfer?.types && this.isTypesValid(t.dataTransfer.items)) {
      this.dragover = true
    } else {
      this.error = true
    }
  }

  onDrop (e:Event) {
    e.preventDefault()
    const transfer = (e as DragEvent).dataTransfer
    if (transfer && transfer.files.length) {
      this.filesSelected(transfer.files)
    }
    this.dragover = false
    this.error = false
  }

  onClick (e:Event) {
    e.preventDefault()
    this.fileInput?.click()
  }

  onKeyPress (e:Event) {
    e.preventDefault()
    if ((e as KeyboardEvent).key === 'Enter') {
      this.fileInput?.click()
    }
  }

  isTypesValid (types: DataTransferItemList) {
    return !this.type || !Array.from(types).find(x => !x.type.startsWith(this.type))
  }

  filterFiles (files: FileList) {
    return Array.from(files).filter(x => x.type && x.size)
  }

  @Emit()
  filesSelected (fileList: FileList) {
    this.dragover = false
    this.error = false
    return this.filterFiles(fileList)
  }
}
</script>
