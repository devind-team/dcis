<template lang="pug">
  v-sheet(height="200" style="cursor:pointer; border:dashed; border-color: gray;")
    v-container(fill-height)
      v-row(justify="center")
        v-icon(v-show="!dragover && !error" size="70") mdi-cloud-upload-outline
        v-icon(v-show="dragover && !error" size="70") mdi-arrow-collapse-down
        v-icon(v-show="error" size="70") mdi-minus-circle
      v-row(justify="center") {{ $t('common.dropFileUpload.dropOrClick') }}
</template>

<script lang="ts">
import { VueConstructor } from 'vue'
import type { PropType } from '#app'
import { defineComponent, getCurrentInstance, onDeactivated, onMounted, ref } from '#app'

export default defineComponent({
  props: {
    type: { type: String as PropType<'text' | 'image' | 'video' | 'application'>, required: true }
  },
  setup (props, { emit }) {
    const instance = getCurrentInstance()
    const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>
    const dragover = ref<boolean>(false)
    const error = ref<boolean>(false)
    const fileInput = ref<HTMLInputElement | null>(null)

    onMounted(() => {
      const fi = document.createElement('input')
      fi.type = 'file'
      fi.multiple = true
      fi.accept = `${props.type}/*`
      fi.onchange = () => {
        filesSelected(fi.files!)
      }
      fileInput.value = fi
      const dropZone = vm.$el
      dropZone.addEventListener('dragenter', onDragEnter)
      dropZone.addEventListener('dragleave', onDragLeave)
      dropZone.addEventListener('dragover', onDragOver)
      dropZone.addEventListener('drop', onDrop)
      dropZone.addEventListener('click', onClick)
      dropZone.addEventListener('keypress', onKeyPress)
    })

    onDeactivated(() => {
      const dropZone = vm.$el
      dropZone.removeEventListener('dragenter', onDragEnter)
      dropZone.removeEventListener('dragleave', onDragLeave)
      dropZone.removeEventListener('dragover', onDragOver)
      dropZone.removeEventListener('drop', onDrop)
      dropZone.removeEventListener('click', onClick)
      dropZone.removeEventListener('keypress', onKeyPress)
    })

    const onDragEnter = (e:Event) => {
      e.preventDefault()
      const t = e as DragEvent
      if (t.dataTransfer?.types && isTypesValid(t.dataTransfer.items)) {
        dragover.value = true
      } else {
        error.value = true
      }
    }

    const onDragLeave = (e:Event) => {
      e.preventDefault()
      dragover.value = false
      error.value = false
    }

    const onDragOver = (e:Event) => {
      e.preventDefault()
      const t = e as DragEvent
      if (t.dataTransfer?.types && isTypesValid(t.dataTransfer.items)) {
        dragover.value = true
      } else {
        error.value = true
      }
    }

    const onDrop = (e:Event) => {
      e.preventDefault()
      const transfer = (e as DragEvent).dataTransfer
      if (transfer && transfer.files.length) {
        filesSelected(transfer.files)
      } else {
        dragover.value = false
        error.value = false
      }
    }

    const onClick = (e:Event) => {
      e.preventDefault()
      fileInput.value?.click()
    }

    const onKeyPress = (e:Event) => {
      e.preventDefault()
      if ((e as KeyboardEvent).key === 'Enter') {
        fileInput.value?.click()
      }
    }

    const isTypesValid = (types: DataTransferItemList) => {
      return !props.type || !Array.from(types).find(x => !x.type.startsWith(props.type))
    }

    const filesSelected = (fileList: FileList) => {
      dragover.value = false
      error.value = false
      emit('files-selected', Array.from(fileList).filter(x => x.type && x.size))
    }
    return { dragover, error }
  }
})
</script>
