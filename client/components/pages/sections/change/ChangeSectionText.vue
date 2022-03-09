<template lang="pug">
  apollo-mutation(
    :mutation="require('~/gql/pages/mutations/section/change_section_text.graphql')"
    :variables="{ sectionId: section.id, text }"
    :update="addSectionDone"
  )
    template(v-slot="{ mutate, loading, error }")
      validation-observer(v-slot="{ handleSubmit, invalid }" ref="changeSection" tag="div")
        v-card
          v-card-text
            v-alert(:value="success" type="success" dismissible) {{$t('mutationSuccess')}}
            v-alert(:value="!!error" type="error" dismissible) {{ error }}
            validation-provider(:name="$t('pages.section.names.text')" rules="required|min:10" v-slot="{ errors }" tag="div")
              rich-text-editor(v-model="text")
              .error--text {{ errors[0] || '' }}
          v-card-actions
            v-checkbox(v-model="toPage" :label="$t('pages.section.toPage')")
            v-spacer
            v-btn(@click="mutate" :loading="loading" :disabled="invalid" color="primary") {{ $t('pages.section.change') }}
</template>

<script lang="ts">
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import {
  ChangeSectionTextMutationPayload,
  ErrorFieldType,
  SectionTextType
} from '~/types/graphql'
import RichTextEditor from '~/components/common/editor/RichTextEditor.vue'

@Component<ChangeSectionText>({
  components: { RichTextEditor }
})
export default class ChangeSectionText extends Vue {
  @Prop({ required: true }) section!: SectionTextType
  @Ref() changeSection!: InstanceType<typeof ValidationObserver>

  toPage: boolean = true
  success: boolean = false
  text!: string

  data () {
    return { text: this.section.text }
  }

  /**
   * Окончание мутации для добавления текстовой секции
   * @param store
   * @param success
   * @param errors
   * @param id Идентификатор новой секции
   */
  addSectionDone (
    store: DataProxy,
    { data: { changeSectionText: { success, errors, section } } }: { data: { changeSectionText: ChangeSectionTextMutationPayload } }
  ) {
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
