<template lang="pug">
  apollo-mutation(
    v-slot="{ mutate, loading, error }"
    :mutation="require('~/gql/pages/mutations/section/add_section_text.graphql')"
    :variables="{ pageId: page.id, text }"
    :update="addSectionDone"
  )
    ValidationObserver(v-slot="{ handleSubmit, invalid }" ref="addSection" tag="div")
      v-card
        v-card-text
          v-alert(:value="!!error" type="error" dismissible) {{ error }}
          ValidationProvider(:name="$t('pages.section.names.text')" rules="required|min:10" v-slot="{ errors }" tag="div")
            rich-text-editor(v-model="text")
            .error--text {{ errors[0] || '' }}
        v-card-actions
          v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
          v-spacer
          v-btn(@click="mutate" :loading="loading" :disabled="invalid" color="primary") {{ $t('pages.section.add') }}
</template>

<script lang="ts">
import { camelCase } from 'scule'
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import { AddSectionTextMutationPayload, ErrorFieldType, PageType } from '~/types/graphql'
import RichTextEditor from '~/components/common/editor/RichTextEditor.vue'

@Component<AddSectionText>({
  components: { RichTextEditor }
})
export default class AddSectionText extends Vue {
  @Prop({ required: true }) page!: PageType
  @Ref() addSection!: InstanceType<typeof ValidationObserver>

  toPage: boolean = true
  text: string = ''

  /**
   * Окончание мутации для добавления текстовой секции
   * @param store
   * @param success
   * @param errors
   * @param id Идентификатор новой секции
   */
  addSectionDone (store: DataProxy, { data: { addSectionText: { success, errors, section } } }: { data: { addSectionText: AddSectionTextMutationPayload } }) {
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
