<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    validation-observer(v-slot="{ handleSubmit, invalid }" slim)
      form(@submit.prevent="handleSubmit(setValue)")
        v-card
          v-card-title {{ t('dcis.cells.gridCellFiles.title') }}
            v-spacer
            v-btn(@click="cancel" icon)
              v-icon mdi-close
          v-card-text
            validation-provider(
              v-slot="{ errors, valid }"
              :name="String(t('dcis.cells.gridCellFiles.fileLink'))"
              rules="required"
            )
              v-text-field(
                v-model="newValue"
                :label="t('dcis.cells.gridCellFiles.fileLink')"
                :error-messages="errors"
                :success="valid"
              )
            validation-provider(
              ref="filesValidationProvider"
              v-slot="{ errors, valid }"
              :custom-messages="{ required: t('dcis.cells.gridCellFiles.filesError') }"
              :detect-input="false"
              rules="required"
            )
              file-field(
                v-for="(file, i) in localValueFiles"
                :key="file.id"
                :lable="t('dcis.cells.gridCellFiles.file', { number: i + 1})"
                :existing-file="{ name: file.name, src: file.src }"
              )
              v-file-input(
                v-model="newFiles"
                :label="t('dcis.cells.gridCellFiles.newFiles')"
                :error-messages="errors"
                :success="valid"
                chips
                clearable
                multiple
              )
          v-card-actions
            v-spacer
            v-btn(:disabled="invalid" type="submit" color="primary") {{ t('save') }}
</template>

<script lang="ts">
import { ValidationProvider } from 'vee-validate'
import { defineComponent, onMounted, ref, computed, watch } from '#app'
import { useI18n, useCommonQuery } from '~/composables'
import { FileType, ValueFilesQuery, ValueFilesQueryVariables } from '~/types/graphql'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'
import FileField from '~/components/common/FileField.vue'

type ValueFile = {
  file: FileType
  deleted: boolean
}

export default defineComponent({
  components: { FileField },
  props: {
    value: { type: String, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const active = ref<boolean>(true)

    const filesValidationProvider = ref<InstanceType<typeof ValidationProvider> | null>(null)

    onMounted(() => {
      filesValidationProvider.value.setFlags({ invalid: true })
    })

    const { data: valueFiles } = useCommonQuery<ValueFilesQuery, ValueFilesQueryVariables, 'valueFiles'>({
      document: valueFilesQuery,
      variables: {
        valueId: props.value
      },
      options: {
        enabled: active.value
      }
    })

    const localValueFiles = ref<ValueFile[]>([])
    watch(valueFiles, (value) => {
      localValueFiles.value = value.map((file: FileType) => ({ file, deleted: false }))
    })

    const remainingExistFiles = computed<string[]>(
      () => localValueFiles.value.filter(valueFile => !valueFile.deleted).map(valueFile => valueFile.file.id)
    )

    const newValue = ref<string>(null)
    const newFiles = ref<File[]>([])

    const remainingFiles = computed<(string | File)[]>(() => [...remainingExistFiles.value, ...newFiles.value])
    watch(remainingFiles, (value) => {
      filesValidationProvider.value.validate(value)
    })

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    const setValue = () => {
      active.value = false
      emit('set-value', newValue.value)
    }

    return {
      t,
      active,
      filesValidationProvider,
      localValueFiles,
      newValue,
      newFiles,
      cancel,
      setValue
    }
  }
})
</script>
