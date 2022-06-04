<template lang="pug">
  mutation-form(
    :mutation="require('~/gql/pages/mutations/section/add_section_files.graphql')"
    :variables="{ pageId: page.id, text, files }"
    :button-text="String($t('pages.section.add'))"
    :update="addSectionDone"
    mutation-name="addSectionFiles"
    i18n-path="pages.section.names"
  )
    template(#form)
      validation-provider(:name="$t('pages.section.names.text')" rules="min:10" v-slot="{ errors }" tag="div")
        v-text-field(v-model="text" :label="$t('pages.section.names.text')" :error-messages="errors")
      drop-file-upload(@files-selected="onFilesSelected")
      v-simple-table(v-show="files.length")
        template(#default)
          thead
            tr
              th {{$t('pages.section.names.files')}}
              th.text-right {{$t('pages.components.sectionGallery.actions')}}
          tbody
            tr(v-for="(file, i) in files" :key="i")
              td {{file.name}}
              td
                v-btn(@click="onFileRemove(i)" icon)
                  v-icon mdi-delete
    template(#actions="{ invalid, loading, buttonText, setFormErrors, setError, setSuccess }")
      v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
      v-spacer
      v-btn(
        :disabled="invalid || !files.length"
        :loading="loading"
        type="submit"
        color="primary"
      ) {{ buttonText }}
</template>

<script lang="ts">
import { defineComponent, ref, PropType, useRouter } from '#app'
import { DataProxy } from 'apollo-cache'
import {
  AddSectionFilesMutationPayload,
  PageType
} from '~/types/graphql'
import DropFileUpload from '~/components/common/DropFileUpload.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'
import { useI18n } from '~/composables'

export default defineComponent({
  components: { DropFileUpload, MutationForm },
  props: { page: { required: true, type: Object as PropType<PageType> } },
  setup (props, { emit }) {
    const { localePath } = useI18n()
    const router = useRouter()

    const toPage = ref(true)
    const text = ref('')
    const files = ref<File[]>([])

    const onFileRemove = (index: number) => {
      files.value.splice(index, 1)
    }

    const onFilesSelected = (_files: File[]) => {
      console.log('_files')
      files.value.push(..._files)
    }

    /**
     * Окончание мутации для добавления текстовой секции
     * @param store
     * @param success
     * @param errors
     * @param id Идентификатор новой секции
     */
    const addSectionDone = (store: DataProxy, { data: { addSectionFiles: { errors, section } } }: { data: { addSectionFiles: AddSectionFilesMutationPayload } }) => {
      if (!errors.length) {
        toPage.value
          ? router.push(localePath({ name: 'pages-pageId', params: { pageId: props.page.id } }))
          : router.push(localePath({
            name: 'pages-pageId-section-sectionId', params: { pageId: props.page.id, sectionId: section!.id as unknown as string }
          }))
        emit('done', store, section)
      }
    }
    return { text, files, toPage, onFileRemove, onFilesSelected, addSectionDone }
  }
})
</script>
