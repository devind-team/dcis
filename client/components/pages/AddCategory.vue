<template lang="pug">
mutation-modal-form(
  @close="close"
  :mutation="require('~/gql/pages/mutations/category/add_category.graphql')"
  :variables="{ avatar, text, parentId: category && category.id }"
  :header="String($t('pages.category.addDialog.header'))"
  :button-text="String($t('pages.category.addDialog.add'))"
  :update="update"
  mutation-name="addCategory"
)
  template(#activator="{ on }")
    slot(:on="on")
      v-card(v-on="on" style="border: 1px rgba(0, 0, 0, 0.12) dashed" ripple outlined)
        v-card-text.text-center
          v-icon mdi-plus
          | {{ $t('pages.category.addCardHeader') }}
  template(#form)
    validation-provider(:name="String($t('pages.category.addDialog.avatar'))" tag="div" v-slot="{ errors, valid }")
      v-file-input(
        v-model="avatar"
        :label="$t('pages.category.addDialog.avatar')"
        :error-messages="errors"
        :success="valid"
        prepend-icon="mdi-camera"
        show-size
      )
    validation-provider(
      :name="String($t('pages.category.addDialog.text'))"
      rules="required|min:3|max:1023"
      v-slot="{ errors, valid }"
    )
      v-text-field(
        v-model="text"
        :label="$t('pages.category.addDialog.text')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
</template>

<script lang="ts">
import type { Ref, PropType } from '#app'
import { defineComponent, ref } from '#app'
import { AddCategoryMutationPayload, CategoryType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

type AddCategoryMutationResult = { data: { addCategory: AddCategoryMutationPayload } }
type AddCategoryUpdate = (cache, DataProxy, result: AddCategoryMutationResult) => void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    category: { type: Object as PropType<CategoryType>, default: null },
    update: { type: Function as PropType<AddCategoryUpdate>, required: true }
  },
  setup (_, { emit }) {
    const avatar: Ref<File | null> = ref<File | null>(null)
    const text: Ref<string> = ref<string>('')

    const close = () => {
      avatar.value = null
      text.value = ''
      emit('close')
    }
    return { avatar, text, close }
  }
})
</script>
