<template lang="pug">
  mutation-form(
    :mutation="require('~/gql/pages/mutations/section/change_section_text.graphql')"
    :variables="{ sectionId: section.id, text }"
    :update="addSectionUpdate"
    :button-text="String($t('pages.section.change'))"
    mutation-name="changeSectionText"
    i18n-path="pages.section.names"
  )
    template(#form)
      validation-provider(:name="String($t('pages.section.names.text'))" rules="required|min:10" v-slot="{ errors }" tag="div")
        rich-text-editor(v-model="text")
        .error--text {{ errors[0] || '' }}
      v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, useRouter, ref, PropType } from '#app'
import { useI18n } from '~/composables'
import { ChangeSectionTextMutationPayload, SectionTextType } from '~/types/graphql'
import RichTextEditor from '~/components/common/editor/RichTextEditor.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

type ChangeSectionTextMutationResult = { data: { changeSectionText: ChangeSectionTextMutationPayload } }

export default defineComponent({
  components: { MutationForm, RichTextEditor },
  props: {
    section: { type: Object as PropType<SectionTextType>, required: true }
  },
  setup (props, { emit }) {
    const router = useRouter()
    const { localePath } = useI18n()
    const text = ref<string>(props.section.text)
    const toPage = ref<boolean>(true)

    const addSectionUpdate = (cache: DataProxy, { data: { changeSectionText: { errors, section } } }: ChangeSectionTextMutationResult) => {
      if (!errors.length) {
        emit('done', cache, section)
        if (toPage.value) {
          router.push(localePath({ name: 'pages-pageId' }))
        }
      }
    }
    return { text, toPage, addSectionUpdate }
  }
})
</script>
