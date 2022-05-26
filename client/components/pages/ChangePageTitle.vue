<template lang="pug">
  mutation-modal-form(
    @done="$emit('close')"
    :mutation="require('~/gql/pages/mutations/page/change_page_title.graphql')"
    :variables="{ pageId: page.id, title }"
    :header="$t('pages.page.changeTitle.header')"
    :button-text="$t('pages.page.changeTitle.change')"
    mutation-name="changePageTitle"
    i18n-path="pages.page.changeTitle"
  )
    template(#activator="{ on }")
      slot(:on="on")
    template(#form)
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
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { PageType } from '~/types/graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: { page: { required: true, type: Object as PropType<PageType> } },
  setup (props) {
    const title = ref(props.page.title)
    return { title }
  }
})
</script>
