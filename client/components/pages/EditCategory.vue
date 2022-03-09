<template lang="pug">
  v-dialog(v-model="drawer" width="600")
    template(v-slot:activator="{ on }")
      slot(:on="on")
    apollo-mutation(
      :mutation="require('~/gql/pages/mutations/category/change_category.graphql')"
      :variables="{ categoryId: category.id, text }"
      :update="update"
      @done="editCategoryDone")
      template(v-slot="{ mutate, loading, error }")
        ValidationObserver(v-slot="{ handleSubmit, invalid }" ref="editCategory")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card
              v-card-title {{ $t('pages.components.editCategory.changeCategory') }}
                v-spacer
                v-btn(@click="close" icon)
                  v-icon mdi-close
              v-card-subtitle(
                v-if="category"
                ) {{ $t('pages.components.editCategory.parentCategory') }} {{ category.text }}
              v-card-text
                v-alert(type="error" :value="!!error" dismissible) {{ error }}
                ValidationProvider(
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
                v-btn(
                  :disabled="invalid"
                  :loading="loading"
                  type="submit"
                  color="primary"
                  ) {{ $t('pages.components.editCategory.change') }}
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { DataProxy } from 'apollo-cache'
import { CategoryType, ChangeCategoryMutationPayload, ErrorFieldType } from '~/types/graphql'

@Component<AddCategory>({})
export default class AddCategory extends Vue {
  drawer: boolean = false
  text!: string

  @Prop({ default: null, type: Object }) category!: CategoryType
  @Prop() update!: (store: DataProxy, result: any) => void

  $refs!: {
    editCategory: InstanceType<typeof ValidationObserver>
  }

  data (): { text: string } {
    return {
      text: this.category.text
    }
  }

  editCategoryDone (
    { data: { changeCategory: { success, errors } } }: { data: { changeCategory: ChangeCategoryMutationPayload } }
  ) {
    if (success) {
      this.close()
    } else {
      this.$refs.editCategory.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.category.addDialog.${this.$snakeToCamel(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }

  close () {
    this.drawer = false
    this.$nextTick(() => { this.$refs.editCategory.reset() })
    this.$emit('close')
  }
}
</script>
