<template lang="pug">
apollo-mutation(
  v-slot="{ mutate, loading, error }"
  :mutation="require('~/gql/pages/mutations/section/change_section_files.graphql')"
  :variables="{ sectionId: section.id, text: section.text, newFiles: files, oldFiles: oldFiles.map(x => x.id) }"
  :update="changeSectionDone"
)
  validation-observer(v-slot="{ handleSubmit, invalid }" ref="changeSection" tag="div")
    v-card
      v-card-text
        v-alert(:value="success" type="success" dismissible) {{$t('mutationSuccess')}}
        v-alert(:value="!!error" type="error" dismissible) {{ error }}
        validation-provider(:name="$t('pages.section.names.text')" rules="min:5" v-slot="{ errors }" tag="div")
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
      v-card-actions
        v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
        v-spacer
        v-btn(@click="mutate" :loading="loading" :disabled="invalid || !files.length && !oldFiles.length" color="primary") {{ $t('pages.section.change') }}
</template>

<script lang="ts">
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import {
  ChangeSectionFilesMutationPayload,
  ErrorFieldType,
  FileType, Maybe, SectionFilesType
} from '~/types/graphql'
import DropFileUpload from '~/components/common/DropFileUpload.vue'

@Component<ChangeSectionFiles>({
  components: { DropFileUpload }
})
export default class ChangeSectionFiles extends Vue {
  @Prop({ required: true }) section!: SectionFilesType
  @Ref() changeSection!: InstanceType<typeof ValidationObserver>

  oldFiles: Maybe<FileType>[] = []
  toPage: boolean = true
  files: File[] = []
  isMenuActive: boolean = false
  success: boolean = false

  mounted () {
    this.oldFiles = [...this.section.files]
  }

  onFileRemove (index: number) {
    this.files.splice(index, 1)
  }

  onOldFileRemove (file: Maybe<FileType>) {
    this.oldFiles.splice(this.oldFiles.indexOf(file), 1)
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
  changeSectionDone (store: DataProxy, { data: { changeSectionFiles: { success, errors, section } } }: { data: { changeSectionFiles: ChangeSectionFilesMutationPayload } }) {
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
