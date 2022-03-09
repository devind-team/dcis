<template lang="pug">
  mutation-modal-form(
    :header="$t('common.richTextEditor.imageUpload')"
    :button-text="$t('common.richTextEditor.image.image')"
    :mutation="require('~/gql/core/mutations/file/add_file.graphql')"
    :variables="{ userId: user.id, files: [image] }"
    @done="onImageUploaded"
    mutation-name="addFile"
  )
    template(#activator="{ on }")
      v-tooltip(top)
        template(#activator="{ on: onTooltip }")
          v-btn(v-on="{ ...on, ...onTooltip }" icon)
            v-icon {{icon}}
        span {{$t('common.richTextEditor.image.image')}}
    template(#form)
      validation-provider(
        v-slot="{ errors, valid }"
        :name="$t('common.richTextEditor.imageField')"
        rules="required"
      )
        v-file-input(
          :label="$t('common.richTextEditor.imageField')"
          v-model="image"
          :success="valid"
          :error-messages="errors"
          clearable
        )
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { Editor } from '@tiptap/core'
import { mapGetters } from 'vuex'
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
    image: null
  }),
  computed: mapGetters({ user: 'auth/user' }),
  methods: {
    onImageUploaded ({ data: { addFile } }: { data: { addFile: AddFileMutationPayload } }): void {
      if (addFile.success) {
        this.editor.chain().focus().setImage({ src: `/${addFile.files[0]!.src}` }).run()
        this.image = null
      }
    }
  }
})
</script>
