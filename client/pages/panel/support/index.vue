<template lang="pug">
bread-crumbs(:items="bc")
  mutation-form(
    :header="String($t('support.header'))"
    :mutation="require('~/gql/core/mutations/support/support_submit.graphql')"
    :variables="{ topic, text, files }"
    :button-text="String($t('send'))"
    :successMessage="String($t('support.successMessage'))"
    mutation-name="supportSubmit"
    errors-in-alert
  )
    template(#form)
      validation-provider(:name="String($t('support.topic'))" rules="required|min:2|max:50" v-slot="{ errors, valid }")
        v-text-field.mb-5(v-model="topic" :label="$t('support.topic')" :error-messages="errors" :success="valid" clearable counter )
      validation-provider(:name="String($t('support.text'))" rules="required|min:2|max:500" v-slot="{ errors, valid }")
        v-textarea(v-model="text" :label="$t('support.text')" :error-messages="errors" :success="valid" counter clearable)
      v-file-input(v-model="files" :label="$t('support.file')" truncate-length="25" multiple show-size)
</template>

<script lang="ts">
import type { ComputedRef, Ref } from '#app'
import { useNuxt2Meta } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n } from '~/composables'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import TwoColumns from '~/components/common/grid/TwoColumns.vue'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { TwoColumns, BreadCrumbs, LeftNavigatorContainer, MutationForm },
  middleware: 'auth',
  setup () {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: t('support.header') as string })

    const topic: Ref<string> = ref<string>('')
    const text: Ref<string> = ref<string>('')
    const files: Ref<File[] | null> = ref<File[] | null>(null)

    const bc: ComputedRef<BreadCrumbsItem[]> = computed(() => ([
      { text: t('panel.index') as string, to: localePath({ name: 'panel' }), exact: true },
      { text: t('support.header') as string, to: localePath({ name: 'panel-support' }), exact: true }
    ]))

    return { bc, topic, text, files }
  }
})
</script>
