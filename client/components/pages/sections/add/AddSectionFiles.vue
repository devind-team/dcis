<template lang="pug">
apollo-mutation(
  v-slot="{ mutate, loading, error }"
  :mutation="require('~/gql/pages/mutations/section/add_section_files.graphql')"
  :variables="{ pageId: page.id, text, files }"
  :update="addSectionDone"
)
  validation-observer(v-slot="{ handleSubmit, invalid }" ref="addSection" tag="div")
    v-card
      v-card-text
        v-alert(:value="!!error" type="error" dismissible) {{ error }}
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
import {
  AddSectionFilesMutationPayload,
  ErrorFieldType,
  PageType
} from '~/types/graphql'
import DropFileUpload from '~/components/common/DropFileUpload.vue'

@Component<AddSectionFiles>({
  components: { DropFileUpload }
})
export default class AddSectionFiles extends Vue {
  @Prop({ required: true }) page!: PageType
  @Ref() addSection!: InstanceType<typeof ValidationObserver>

  toPage: boolean = true
  text: string = ''
  files: File[] = []
  index: number | null = null
  isMenuActive: boolean = false

  onFileRemove (index: number) {
    this.files.splice(index, 1)
  }

  onFilesSelected (files: File[]) {
    this.files.push(...files)
  }

  /**
   * Окончание мутации для добавления текстовой секции
   * @param store
   * @param success
   * @param errors
   * @param id Идентификатор новой секции
   */
  addSectionDone (store: DataProxy, { data: { addSectionFiles: { success, errors, section } } }: { data: { addSectionFiles: AddSectionFilesMutationPayload } }) {
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
