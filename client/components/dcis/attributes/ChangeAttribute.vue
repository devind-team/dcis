<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.attributes.changeMenu.header'))"
  :mutation="require('~/gql/dcis/mutations/attributes/change_attribute.graphql')"
  :button-text="String($t('dcis.attributes.changeMenu.buttonText'))"
  :variables="{ id: attribute.id, name, placeholder, key, kind: kind.toLowerCase(), 'default': def, mutable  }"
  :update="update"
  i18n-path="dcis.attributes.changeMenu"
  mutation-name="changeAttribute"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="default" :on="on")
  template(#form)
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.changeMenu.name'))" rules="required")
      v-text-field(v-model="name" :error-messages="errors" :label="String($t('dcis.attributes.changeMenu.name'))" :success="valid" autofocus)
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.changeMenu.placeholder'))" rules="required")
      v-text-field(v-model="placeholder" :error-messages="errors" :label="String($t('dcis.attributes.changeMenu.placeholder'))" :success="valid")
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.changeMenu.key'))" rules="required")
      v-text-field(v-model="key" :error-messages="errors" :label="String($t('dcis.attributes.changeMenu.key'))" :success="valid")
    validation-provider(v-slot="{ errors, valid }" :name="String($t('dcis.attributes.changeMenu.kind'))" rules="required")
      v-select(v-model="kind" :items="kinds" :label="String($t('dcis.attributes.changeMenu.kind'))" :error-messages="errors" :success="valid")
    v-text-field(v-model="def" :label="String($t('dcis.attributes.changeMenu.default'))")
    v-checkbox(v-model="mutable" :label="String($t('dcis.attributes.changeMenu.mutable'))")
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { DataProxy } from 'apollo-cache'
import { useI18n } from '~/composables'
import { AttributeKind, AttributeType, ChangeAttributeMutationPayload } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import { getAttributeKinds } from '~/components/dcis/attributes/AddAttributeMenu.vue'

export type ChangeAttributeMutationResult = { data: { changeAttribute: ChangeAttributeMutationPayload }}

export default defineComponent({
  components: { MutationModalForm },
  props: {
    attribute: { type: Object as PropType<AttributeType>, required: true },
    update: { type: Function as PropType<(cache: DataProxy, result: ChangeAttributeMutationResult) => void> }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const name = ref<string>(props.attribute.name)
    const placeholder = ref<string>(props.attribute.placeholder)
    const def = ref<string>(props.attribute.default)
    const key = ref<string>(props.attribute.key)
    const kind = ref<AttributeKind>(props.attribute.kind)
    const mutable = ref<boolean>(props.attribute.mutable)

    const kinds = getAttributeKinds(t)

    const close = () => {
      emit('close')
    }

    return {
      name,
      placeholder,
      def,
      key,
      kind,
      mutable,
      kinds,
      close
    }
  }
})
</script>
