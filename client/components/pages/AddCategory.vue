<template lang="pug">
  v-dialog(v-model="drawer" width="600")
    template(#activator="{ on }")
      slot(:on="on")
        v-card(v-on="on" style="border: 1px rgba(0, 0, 0, 0.12) dashed" ripple outlined)
          v-card-text.text-center
            v-icon mdi-plus
            | {{ $t('pages.category.addCardHeader') }}
    apollo-mutation(
      :mutation="require('~/gql/pages/mutations/category/add_category.graphql')"
      :variables="{ avatar, text, parentId: category && category.id }"
      :update="update"
      :refetchQueries="refetchQueries"
      @done="addCategoryDone"
      v-slot="{ mutate, loading, error }"
    )
      validation-observer(v-slot="{ handleSubmit, invalid }" ref="addCategory")
        form(@submit.prevent="handleSubmit(mutate)")
          v-card
            v-card-title {{ $t('pages.category.addDialog.header') }}
              v-spacer
              v-btn(@click="close" icon)
                v-icon mdi-close
            v-card-subtitle(v-if="category") {{ $t('pages.category.addDialog.parentCategory') + category.text }}
            v-card-text
              v-alert(type="error" :value="!!error" dismissible) {{ error }}
              validation-provider(:name="$t('pages.category.addDialog.avatar')" tag="div" v-slot="{ errors, valid }")
                v-file-input(
                  v-model="avatar"
                  :label="$t('pages.category.addDialog.avatar')"
                  :error-messages="errors"
                  :success="valid"
                  prepend-icon="mdi-camera"
                  show-size
                )
              validation-provider(
                :name="$t('pages.category.addDialog.text')"
                rules="required|min:3|max:1023"
                v-slot="{ errors, valid }"
              )
                v-text-field(
                  v-model="text"
                  :label="$t('pages.category.addDialog.text')"
                  :error-messages="errors"
                  :success="valid"
                )
            v-card-actions
              v-spacer
              v-btn(:disabled="invalid" :loading="loading" type="submit" color="primary")
                | {{ $t('pages.category.addDialog.add') }}
</template>

<script lang="ts">
import { Vue, Component, Prop, Ref } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import { CategoryType, ErrorFieldType, AddCategoryMutation } from '~/types/graphql'

@Component<AddCategory>({})
export default class AddCategory extends Vue {
  @Prop({ default: null, type: Object }) category!: CategoryType
  @Prop({ required: true, type: Function }) update!: (store: DataProxy, result: any) => void
  @Prop() refetchQueries!: () => { query: any, variables: any }[]

  @Ref() readonly addCategory!: InstanceType<typeof ValidationObserver>

  drawer: boolean = false
  avatar: File | null = null
  text: string = ''
  parentId: string | null = null

  addCategoryDone ({ data: { addCategory: { success, errors } } }: { data: AddCategoryMutation }) {
    if (success) {
      this.close()
    } else {
      this.addCategory.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.addDialog.category.${this.$snakeToCamel(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }

  close () {
    this.drawer = false
    this.avatar = null
    this.text = ''
    this.$nextTick(() => { this.addCategory.reset() })
    this.$emit('close')
  }
}
</script>
