<template lang="pug">
  mutation-form(
    :mutation="require('~/gql/pages/mutations/section/change_section_gallery.graphql')"
    :variables="{ sectionId: section.id, text: section.text, newImages: files, oldImages: oldImages.map(x => x.id) }"
    :update="changeSectionDone"
    :button-text="String($t('pages.section.change'))"
    mutation-name="changeSectionGallery"
    i18n-path="pages.section.names"
  )
    template(#form)
      validation-provider(:name="$t('pages.section.names.text')" rules="min:5" v-slot="{ errors }" tag="div")
        v-text-field(v-model="section.text" :label="$t('pages.section.names.text')" :error-messages="errors")
      drop-file-upload(type="image" @files-selected="onFilesSelected")
      v-simple-table(v-show="preview.length || oldImages.length")
        template(#default)
          thead
            tr
              th {{$t('pages.components.sectionGallery.images')}}
              th.text-right {{$t('pages.components.sectionGallery.actions')}}
          tbody
            tr(v-for="(image) in oldImages" :key="image.id")
              td
                img(width="50" :src="`/${image.src}`")
              td
                v-btn(@click="onOldImageRemove(image)" icon)
                  v-icon mdi-delete
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
        :disabled="invalid || !files.length && !oldImages.length"
        :loading="loading"
        type="submit"
        color="primary"
      ) {{ buttonText }}
</template>

<script lang="ts">
import { defineComponent, ref, PropType, useRouter } from '#app'
import { DataProxy } from 'apollo-cache'
import {
  ChangeSectionGalleryMutationPayload,
  FileType, Maybe,
  SectionGalleryType
} from '~/types/graphql'
import { useI18n } from '~/composables'
import ImageGallery from '~/components/common/ImageGallery.vue'
import DropFileUpload from '~/components/common/DropFileUpload.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { ImageGallery, DropFileUpload, MutationForm },
  props: { section: { required: true, type: Object as PropType<SectionGalleryType> } },
  setup (props, { emit }) {
    const { localePath } = useI18n()
    const router = useRouter()
    const oldImages = ref<Maybe<FileType>[]>([...props.section.images])
    const toPage = ref(true)
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

    const onOldImageRemove = (image: Maybe<FileType>) => {
      oldImages.value.splice(oldImages.value.indexOf(image), 1)
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
    const changeSectionDone = (store: DataProxy, { data: { changeSectionGallery: { section, errors } } }: { data: { changeSectionGallery: ChangeSectionGalleryMutationPayload } }) => {
      if (!errors.length) {
        emit('done', store, section)
        if (toPage.value) {
          router.push(localePath({ name: 'pages-pageId' }))
        }
      }
    }
    return { files, oldImages, toPage, preview, changeSectionDone, onFilesSelected, onOldImageRemove, onImageRemove }
  }
})
</script>
