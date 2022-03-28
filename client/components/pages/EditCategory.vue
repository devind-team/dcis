<template lang="pug">
  mutation-modal-form(
    @close="$emit('close')"
    :mutation="require('~/gql/pages/mutations/category/change_category.graphql')"
    :variables="{ categoryId: category.id, text }"
    :update="update"
    :header="String($t('pages.components.editCategory.changeCategory'))"
    :button-text="String($t('pages.components.editCategory.change'))"
    mutation-name="changeCategory"
  )
    template(#activator="{ on }")
      slot(:on="on")
    template(#form)
      ValidationProvider(
        :name="String($t('pages.category.addDialog.text'))"
        rules="required|min:3|max:1023"
        v-slot="{ errors, valid }"
      )
        v-text-field(
          v-model="text"
          :label="$t('pages.category.addDialog.text')"
          :error-messages="errors"
          :success="valid"
        )
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { Ref, PropType } from '#app'
import { defineComponent, ref } from '#app'
import { CategoryType, ChangeCategoryMutationPayload } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

type ChangeCategoryUpdate = (cache: DataProxy, result: { data: { changeCategory: ChangeCategoryMutationPayload } }) => void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    category: { type: Object as PropType<CategoryType>, required: true },
    update: { type: Function as PropType<ChangeCategoryUpdate>, required: true }
  },
  setup (props) {
    const text: Ref<string> = ref<string>(props.category.text)
    return { text }
  }
})
</script>
