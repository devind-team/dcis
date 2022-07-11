<template lang="pug">
mutation-form(
  :mutation="require('~/gql/pages/mutations/section/add_section_gallery.graphql')"
  :variables="{ pageId: page.id, text, images: files }"
  :button-text="String($t('pages.section.add'))"
  :update="addSectionDone"
  mutation-name="addSectionGallery"
  i18n-path="pages.section.names"
)
  template(#form)
    validation-provider(:name="$t('pages.section.names.text')" rules="min:10" v-slot="{ errors }" tag="div")
     v-text-field(v-model="text" :label="$t('pages.section.names.text')" :error-messages="errors")
    drop-file-upload(type="image" @files-selected="onFilesSelected")
    v-simple-table(v-show="preview.length")
      template(#default)
        thead
          tr
            th {{$t('pages.components.sectionGallery.images')}}
            th.text-right {{$t('pages.components.sectionGallery.actions')}}
        tbody
          tr(v-for="(image, i) in preview" :key="i")
            td
              img(width="50" :src="image")
            td
              v-btn(@click="onImageRemove(i)" icon)
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
import { AddSectionGalleryMutationPayload, PageType } from '~/types/graphql'
import ImageGallery from '~/components/common/ImageGallery.vue'
import DropFileUpload from '~/components/common/DropFileUpload.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'
import { useI18n } from '~/composables'

export default defineComponent({
  components: { ImageGallery, DropFileUpload, MutationForm },
  props: { page: { required: true, type: Object as PropType<PageType> } },
  setup (props, { emit }) {
    const { localePath } = useI18n()
    const router = useRouter()

    const toPage = ref(true)
    const text = ref('')
    const files = ref<File[]>([])
    const preview = ref<string[]>([])

    const imgSrc = (input: File) => {
      return new Promise<string>((resolve, reject) => {
        const imgUrl: string | ArrayBuffer | null = ''
        if (!input) {
          reject(imgUrl)
          return
        }
        const reader = new FileReader()
        reader.onload = (e) => {
          resolve(e.target?.result as string)
        }
        reader.readAsDataURL(input)
      })
    }

    const refresh = async () => {
      const previweImgs = []
      for (const f of files.value) {
        previweImgs.push(await imgSrc(f))
      }
      preview.value = previweImgs
    }

    const onImageRemove = async (index: number) => {
      files.value.splice(index, 1)
      await refresh()
    }

    const onFilesSelected = async (_files: File[]) => {
      files.value.push(..._files)
      await refresh()
    }

    /**
     * Окончание мутации для добавления текстовой секции
     * @param store
     * @param success
     * @param errors
     * @param id Идентификатор новой секции
     */
    const addSectionDone = (store: DataProxy, { data: { addSectionGallery: { errors, section } } }: { data: { addSectionGallery: AddSectionGalleryMutationPayload } }) => {
      if (!errors.length) {
        toPage.value
          ? router.push(localePath({ name: 'pages-pageId', params: { pageId: props.page.id } }))
          : router.push(localePath({
            name: 'pages-pageId-section-sectionId', params: { pageId: props.page.id, sectionId: section!.id as unknown as string }
          }))
        emit('done', store, section)
      }
    }
    return { text, files, preview, toPage, addSectionDone, onImageRemove, onFilesSelected }
  }
})
</script>
