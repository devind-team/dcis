<template lang="pug">
  mutation-form(
    :mutation="require('~/gql/pages/mutations/section/add_section_text.graphql')"
    :variables="{ pageId: page.id, text }"
    :update="addSectionDone"
    :button-text="$t('pages.section.add')"
    mutation-name="addSectionText"
    i18n-path="pages.section.names"
  )
    template(#form)
      validation-provider(:name="$t('pages.section.names.text')" rules="required|min:10" v-slot="{ errors }" tag="div")
        rich-text-editor(v-model="text")
        .error--text {{ errors[0] || '' }}
    template(#actions="{ invalid, loading, buttonText, setFormErrors, setError, setSuccess }")
      v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
      v-spacer
      v-btn(
        :disabled="invalid"
        :loading="loading"
        type="submit"
        color="primary"
      ) {{ buttonText }}
</template>

<script lang="ts">
import { camelCase } from 'scule'
import { defineComponent, PropType, ref, useRouter } from '#app'
import { DataProxy } from 'apollo-cache'
import { ValidationObserver } from 'vee-validate'
import { useAuthStore } from '~/stores'
import { useI18n } from '~/composables'
import { AddSectionTextMutationPayload, ErrorFieldType, PageType } from '~/types/graphql'
import RichTextEditor from '~/components/common/editor/RichTextEditor.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm, RichTextEditor },
  props: { page: { required: true, type: Object as PropType<PageType> } },
  setup (props, { emit }) {
    const { t, localePath } = useI18n()
    const router = useRouter()
    const addSection = ref<InstanceType<typeof ValidationObserver>>(null)

    const toPage = ref(true)
    const text = ref('')

    /**
     * Окончание мутации для добавления текстовой секции
     * @param store
     * @param success
     * @param errors
     * @param id Идентификатор новой секции
     */
    const addSectionDone = (store: DataProxy, { data: { addSectionText: { success, errors, section } } }: { data: { addSectionText: AddSectionTextMutationPayload } }) => {
      if (success) {
        toPage.value
          ? router.push(localePath({ name: 'pages-pageId', params: { pageId: props.page.id } }))
          : router.push(localePath({
            name: 'pages-pageId-section-sectionId', params: { pageId: props.page.id, sectionId: section!.id as unknown as string }
          }))
        emit('done', store, section)
      } else {
        addSection.value.setErrors(errors.reduce(
          (a: { [key: string]: string[] }, c: ErrorFieldType) => {
            return { ...a, [t(`pages.section.names.${camelCase(c.field)}`) as string]: c.messages }
          }, {}))
      }
    }
    return { toPage, text, addSectionDone }
  }
})
</script>
