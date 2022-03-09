<template lang="pug">
apollo-mutation(
  v-slot="{ mutate, loading, error }"
  :mutation="require('~/gql/pages/mutations/section/change_section_gallery.graphql')"
  :variables="{ sectionId: section.id, text: section.text, newImages: files, oldImages: oldImages.map(x => x.id) }"
  :update="changeSectionDone"
)
  validation-observer(v-slot="{ handleSubmit, invalid }" ref="changeSection" tag="div")
    v-card
      v-card-text
        v-alert(:value="success" type="success" dismissible) {{$t('mutationSuccess')}}
        v-alert(:value="!!error" type="error" dismissible) {{ error }}
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
      v-card-actions
        v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
        v-spacer
        v-btn(@click="mutate" :loading="loading" :disabled="invalid || !files.length && !oldImages.length" color="primary") {{ $t('pages.section.change') }}
</template>

<script lang="ts">
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import {
  ChangeSectionGalleryMutationPayload,
  ErrorFieldType,
  FileType, Maybe,
  SectionGalleryType
} from '~/types/graphql'
import ImageGallery from '~/components/common/ImageGallery.vue'
import DropFileUpload from '~/components/common/DropFileUpload.vue'

@Component<ChangeSectionGallery>({
  components: { ImageGallery, DropFileUpload }
})
export default class ChangeSectionGallery extends Vue {
  @Prop({ required: true }) section!: SectionGalleryType
  @Ref() changeSection!: InstanceType<typeof ValidationObserver>

  oldImages: Maybe<FileType>[] = []
  toPage: boolean = true
  files: File[] = []
  preview: string[] = []
  isMenuActive: boolean = false
  success: boolean = false

  mounted () {
    this.oldImages = [...this.section.images]
  }

  imgSrc (input: File) {
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

  async refresh () {
    const previweImgs = []
    for (const f of this.files) {
      previweImgs.push(await this.imgSrc(f))
    }
    this.preview = previweImgs
  }

  async onImageRemove (index: number) {
    this.files.splice(index, 1)
    await this.refresh()
  }

  onOldImageRemove (image: Maybe<FileType>) {
    this.oldImages.splice(this.oldImages.indexOf(image), 1)
  }

  async onFilesSelected (files: File[]) {
    this.files.push(...files)
    await this.refresh()
  }

  /**
   * Окончание мутации для добавления текстовой секции
   * @param store
   * @param success
   * @param errors
   * @param id Идентификатор новой секции
   */
  changeSectionDone (store: DataProxy, { data: { changeSectionGallery: { success, errors, section } } }: { data: { changeSectionGallery: ChangeSectionGalleryMutationPayload } }) {
    if (success) {
      this.success = true
      setTimeout(() => { this.success = false }, 2000)
      this.$emit('done', store, section)
      if (this.toPage) {
        this.$router.push(this.localePath({ name: 'pages-pageId' }))
      }
    } else {
      this.changeSection.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.section.names.${this.$snakeToCamel(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }
}
</script>
