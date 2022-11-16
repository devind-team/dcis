<template lang="pug">
mutation-form(
  :mutation="require('~/gql/pages/mutations/section/change_section_files.graphql')"
  :variables="{ sectionId: section.id, text: section.text, newFiles: files, oldFiles: oldFiles.map(x => x.id) }"
  :update="changeSectionDone"
  :button-text="String($t('pages.section.change'))"
  mutation-name="changeSectionFiles"
  i18n-path="pages.section.names"
)
  template(#form)
    validation-provider(:name="String($t('pages.section.names.text'))" rules="min:5" v-slot="{ errors }" tag="div")
      v-text-field(v-model="section.text" :label="$t('pages.section.names.text')" :error-messages="errors")
    drop-file-upload(@files-selected="onFilesSelected")
    v-simple-table(v-show="files.length || oldFiles.length")
      template(#default)
        thead
          tr
            th {{$t('pages.section.names.files')}}
            th.text-right {{$t('pages.components.sectionGallery.actions')}}
        tbody
          tr(v-for="file in oldFiles" :key="file.id")
            td
              a(:href="file.src") {{ file.name }}
            td
              v-btn(@click="onOldFileRemove(file)" icon)
                v-icon mdi-delete
          tr(v-for="(file, i) in files" :key="i")
            td {{ file.name }}
            td
              v-btn(@click="onFileRemove(i)" icon)
                v-icon mdi-delete
  template(#actions="{ invalid, loading, buttonText, setFormErrors, setError, setSuccess }")
    v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
    v-spacer
    v-btn(
      :disabled="invalid || !files.length && !oldFiles.length"
      :loading="loading"
      type="submit"
      color="primary"
    ) {{ buttonText }}
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from '#app'
import { DataProxy } from 'apollo-cache'
import {
  ChangeSectionFilesMutationPayload,
  FileType, Maybe, SectionFilesType
} from '~/types/graphql'
import { useI18n } from '~/composables'
import DropFileUpload from '~/components/common/DropFileUpload.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { DropFileUpload, MutationForm },
  props: { section: { required: true, type: Object as PropType<SectionFilesType> } },
  setup (props, { emit }) {
    const { localePath } = useI18n()
    const router = useRouter()

    const oldFiles = ref<Maybe<FileType>[]>([...props.section.files])
    const toPage = ref(true)
    const files = ref<File[]>([])

    const onFileRemove = (index: number) => {
      files.value.splice(index, 1)
    }

    const onOldFileRemove = (file: Maybe<FileType>) => {
      oldFiles.value.splice(oldFiles.value.indexOf(file), 1)
    }

    const onFilesSelected = (_files: File[]) => {
      files.value.push(..._files)
    }

    /**
     * Окончание мутации для добавления текстовой секции
     * @param store
     * @param success
     * @param errors
     * @param id Идентификатор новой секции
     */
    const changeSectionDone = (store: DataProxy, { data: { changeSectionFiles: { errors, section } } }: { data: { changeSectionFiles: ChangeSectionFilesMutationPayload } }) => {
      if (!errors.length) {
        emit('done', store, section)
        if (toPage.value) {
          router.push(localePath({ name: 'pages-pageId' }))
        }
      }
    }
    return { files, oldFiles, toPage, onFilesSelected, onFileRemove, onOldFileRemove, changeSectionDone }
  }
})
</script>
