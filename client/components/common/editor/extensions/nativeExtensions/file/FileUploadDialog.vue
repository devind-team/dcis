<template lang="pug">
  mutation-modal-form(
    :header="$t('common.richTextEditor.fileUpload')"
    :button-text="$t('common.richTextEditor.file')"
    :mutation="require('~/gql/core/mutations/file/add_file.graphql')"
    :variables="{ userId: user.id, files: [file] }"
    @done="onFileUploaded"
    mutation-name="addFile"
  )
    template(#activator="{ on }")
      v-tooltip(top)
        template(#activator="{ on: onTooltip }")
          v-btn(v-on="{ ...on, ...onTooltip }" icon)
            v-icon {{icon}}
        span {{$t('common.richTextEditor.file')}}
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="$t('common.richTextEditor.fileLabelField')"
        rules="required"
      )
        v-text-field(
          :label="$t('common.richTextEditor.fileLabelField')"
          v-model="fileLabel"
          :success="valid"
          :error-messages="errors"
          clearable
        )
      validation-provider(
        v-slot="{ errors, valid }"
        :name="$t('common.richTextEditor.fileField')"
        rules="required"
      )
        v-file-input(
          :label="$t('common.richTextEditor.fileField')"
          v-model="file"
          :success="valid"
          :error-messages="errors"
          @change="onFileChanged"
          clearable
        )
</template>
<script lang="ts">
import Vue, { PropType } from 'vue'
import { mapGetters } from 'vuex'
import { Editor } from '@tiptap/core'
import { OnButtonStateChangedType, OnClickType } from '~/components/common/editor/extensions/ExtensionOptionsInterface'
import { AddFileMutationPayload } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default Vue.extend<any, any, any, any>({
  components: { MutationModalForm },
  props: {
    tooltip: { type: String, required: true },
    icon: { type: String, required: true },
    editor: { type: Object as PropType<Editor>, required: true },
    onClick: { type: Function as PropType<OnClickType>, default: () => null },
    isDisabled: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isActive: { type: Function as PropType<OnButtonStateChangedType>, default: () => null },
    isVisible: { type: Function as PropType<OnButtonStateChangedType>, default: () => null }
  },
  data: () => ({
    file: null,
    fileLabel: ''
  }),
  computed: mapGetters({ user: 'auth/user' }),
  methods: {
    onFileUploaded ({ data: { addFile } }: { data: { addFile: AddFileMutationPayload } }): void {
      if (addFile.success) {
        this.editor.chain().focus()
          .insertContent(`<a href="/${addFile.files[0]!.src}" target="_blank">${this.fileLabel}</a>`).run()
        this.file = null
        this.fileLabel = ''
      }
    },
    onFileChanged (file: File | null) {
      if (file) {
        this.fileLabel = file.name
      }
    }
  }
})
</script>
