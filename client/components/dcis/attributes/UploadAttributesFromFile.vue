<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.attributes.uploadAttributes.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.attributes.uploadAttributes.buttonText'))"
  :mutation="uploadAttributesFromFileMutation"
  :variables="variables"
  :update="update"
  mutation-name="uploadAttributesFromFile"
  i18n-path="dcis.attributes.uploadAttributes"
  @close="close"
)
  template(#activator="{ on, attrs}")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.attributes.uploadAttributes.attributesFile'))"
      rules="required"
    )
      v-file-input(
        v-model="attributesFile"
        :label="$t('dcis.attributes.uploadAttributes.attributesFile')"
        :error-messages="errors"
        :success="valid"
        accept=".json"
     )
        template(#append-outer)
          v-tooltip(bottom)
            template(#activator="{ on, attrs }")
              v-btn(v-bind="attrs" v-on="on" href="/templates/Атребуты.json" small icon download)
                v-icon mdi-file-download
            span {{ $t('dcis.attributes.uploadAttributes.downloadTemplate') }}
</template>

<script lang="ts">
import { defineComponent, PropType, computed } from '#app'
import { ResetUpdateType } from '~/composables'
import { PeriodType, UploadAttributesFromFileMutationVariables } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import uploadAttributesFromFileMutation from '~/gql/dcis/mutations/attributes/upload_attributes_from_file.graphql'

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<ResetUpdateType>, required: true }
  },
  setup (props) {
    const attributesFile = ref<File | null>(null)

    const variables = computed<UploadAttributesFromFileMutationVariables>(() => ({
      periodId: props.period.id,
      attributesFile: attributesFile.value
    }))

    const close = () => {
      attributesFile.value = null
    }

    return {
      uploadAttributesFromFileMutation,
      attributesFile,
      variables,
      close
    }
  }
})
</script>
