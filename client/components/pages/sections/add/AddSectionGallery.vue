<template lang="pug">
apollo-mutation(
  v-slot="{ mutate, loading, error }"
  :mutation="require('~/gql/pages/mutations/section/add_section_gallery.graphql')"
  :variables="{ pageId: page.id, text, images: files }"
  :update="addSectionDone"
)
  validation-observer(v-slot="{ handleSubmit, invalid }" ref="addSection" tag="div")
    v-card
      v-card-text
        v-alert(:value="!!error" type="error" dismissible) {{ error }}
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
      v-card-actions
        v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
        v-spacer
        v-btn(@click="mutate" :loading="loading" :disabled="invalid || !files.length" color="primary") {{ $t('pages.section.add') }}
</template>

<script lang="ts">
import { camelCase } from 'scule'
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import { AddSectionGalleryMutationPayload, ErrorFieldType, PageType } from '~/types/graphql'
import ImageGallery from '~/components/common/ImageGallery.vue'
import DropFileUpload from '~/components/common/DropFileUpload.vue'

@Component<AddSectionGallery>({
  components: { ImageGallery, DropFileUpload }
})
export default class AddSectionGallery extends Vue {
  @Prop({ required: true }) page!: PageType
  @Ref() addSection!: InstanceType<typeof ValidationObserver>

  toPage: boolean = true
  text: string = ''
  files: File[] = []
  preview: string[] = []
  index: number | null = null
  isMenuActive: boolean = false

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
  addSectionDone (store: DataProxy, { data: { addSectionGallery: { success, errors, section } } }: { data: { addSectionGallery: AddSectionGalleryMutationPayload } }) {
    if (success) {
      this.toPage
        ? this.$router.push(this.localePath({ name: 'pages-pageId', params: { pageId: this.page.id } }))
        : this.$router.push(this.localePath({
          name: 'pages-pageId-section-sectionId', params: { pageId: this.page.id, sectionId: section!.id as unknown as string }
        }))
      this.$emit('done', store, section)
    } else {
      this.addSection.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.section.names.${camelCase(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }
}
</script>
