<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.attributes.addMenu.header'))"
  :subheader="period.name"
  :mutation="require('~/gql/dcis/mutations/attributes/add_attribute.graphql')"
  :button-text="String($t('dcis.attributes.addMenu.buttonText'))"
  :variables="{ period: period.id, name, placeholder, key, kind: kind.toLowerCase(), default: def, mutable }"
  :update="update"
  mutation-name="addAttribute"
  i18n-path="dcis.attributes.addMenu"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.addMenu.name'))" rules="required")
      v-text-field(v-model="name" :error-messages="errors" :label="String($t('dcis.attributes.addMenu.name'))" :success="valid" autofocus)
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.addMenu.placeholder'))" rules="required")
      v-text-field(v-model="placeholder" :error-messages="errors" :label="String($t('dcis.attributes.addMenu.placeholder'))" :success="valid")
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.addMenu.key'))" rules="required")
      v-text-field(v-model="key" :error-messages="errors" :label="String($t('dcis.attributes.addMenu.key'))" :success="valid")
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.addMenu.kind'))" rules="required")
      v-select(v-model="kind" :items="kinds" :label="String($t('dcis.attributes.addMenu.kind'))" :error-messages="errors" :success="valid")
    v-text-field(v-model="def" :label="String($t('dcis.attributes.addMenu.default'))")
    v-checkbox(v-model="mutable" :label="String($t('dcis.attributes.addMenu.mutable'))")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, PropType, ref } from '#app'
import { useI18n } from '~/composables'
import { AddAttributeMutationPayload, AttributeKind, PeriodType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { getAttributeKinds } from '~/components/dcis/attributes/AddAttributeMenu.vue'

export type AddAttributeMutationResult = { data: { addAttribute: AddAttributeMutationPayload } }

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: {
      type: Function as PropType<(cache: DataProxy, result: AddAttributeMutationResult) => void>,
      required: true
    }
  },
  setup (_, { emit }) {
    const { t } = useI18n()

    const name = ref<string>('')
    const placeholder = ref<string>('')
    const key = ref<string>('')
    const kind = ref<AttributeKind>('TEXT')
    const def = ref<string>('')
    const mutable = ref<boolean>(true)

    const kinds = getAttributeKinds(t)

    const close = () => {
      name.value = ''
      placeholder.value = ''
      key.value = ''
      kind.value = 'TEXT'
      def.value = ''
      mutable.value = true
      emit('close')
    }

    return {
      name,
      placeholder,
      key,
      kind,
      def,
      mutable,
      kinds,
      close
    }
  }
})
</script>
