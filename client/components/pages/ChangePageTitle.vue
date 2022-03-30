<template lang="pug">
  v-dialog(v-model="drawer" width="600")
    template(#activator="{ on }")
      slot(:on="on")
    apollo-mutation(
      :mutation="require('~/gql/pages/mutations/page/change_page_title.graphql')"
      :variables="{ pageId: page.id, title }"
      @done="changePageTitleDone"
      v-slot="{ mutate, loading, error }"
    )
      validation-observer(v-slot="{ handleSubmit, invalid }" ref="changePageTitle")
        form(@submit.prevent="handleSubmit(mutate)")
          v-card
            v-card-title {{ $t('pages.page.changeTitle.header') }}
              v-spacer
              v-btn(@click="close" icon)
                v-icon mdi-close
            v-card-text
              v-alert(type="error" :value="!!error" dismissible) {{ error }}
              validation-provider(
                :name="$t('pages.page.changeTitle.text')"
                rules="required|min:3|max:1023"
                v-slot="{ errors, valid }"
              )
                v-text-field(
                  v-model="title"
                  :label="$t('pages.page.changeTitle.text')"
                  :error-messages="errors"
                  :success="valid"
                )
            v-card-actions
              v-spacer
              v-btn(
                :disabled="invalid"
                :loading="loading"
                type="submit"
                color="primary"
              ) {{ $t('pages.page.changeTitle.change') }}
</template>

<script lang="ts">
import { camelCase } from 'scule'
import { Component, Prop, Ref, Vue } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { ChangePageTitleMutation, ErrorFieldType, PageType } from '~/types/graphql'

@Component<ChangePageTitle>({})
export default class ChangePageTitle extends Vue {
  @Prop({ required: true, type: Object }) readonly page!: PageType

  @Ref() readonly changePageTitle!: InstanceType<typeof ValidationObserver>

  drawer: boolean = false
  title!: string

  data () {
    return {
      title: this.page.title
    }
  }

  changePageTitleDone ({ data: { changePageTitle: { success, errors } } }: { data: ChangePageTitleMutation }) {
    if (success) {
      this.close()
    } else {
      this.changePageTitle.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.page.changeTitle.${camelCase(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }

  close () {
    this.drawer = false
    this.title = this.page.title
    this.$nextTick(() => { this.changePageTitle.reset() })
    this.$emit('close')
  }
}
</script>
