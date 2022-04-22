<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    validation-observer(v-slot="{ invalid }" slim)
      form
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
              v-list(v-if="localValueFiles.length" dense)
                v-list-item.px-0(
                   v-for="localFile in localValueFiles"
                   :key="localFile.file.id"
                   dense
                )
                  v-list-item-action
                    v-tooltip(bottom)
                      template(#activator="{ on, attrs }")
                        v-btn(
                          v-bind="attrs"
                          v-on="on"
                          color="red"
                          small
                          icon
                          role="checkbox"
                          :aria-checked="localFile.deleted"
                          @click="localFile.deleted = !localFile.deleted"
                        )
                          v-icon(size="22") {{ localFile.deleted ? 'mdi-delete-off' : 'mdi-delete' }}
                      span {{ localFile.deleted ? t('cancelDeletion') : t('delete') }}
                  v-list-item-content
                    v-list-item-title
                      nuxt-link(
                        :to="`/${localFile.file.src}`"
                        :class="{'text-decoration-line-through': localFile.deleted}"
                        target="_blank"
                      ) {{ localFile.file.name }}
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
            v-btn(color="error" @click="clearValue") {{ t('clear') }}
            v-spacer
            v-btn(:disabled="invalid" type="submit" color="primary" @click="setValue") {{ t('save') }}
</template>

<script lang="ts">
import { ValidationProvider } from 'vee-validate'
import { defineComponent, onMounted, ref, computed, watch } from '#app'
import type { PropType } from '#app'
import { useI18n, useCommonQuery } from '~/composables'
import {
  FileType,
  ValueType,
  ValueFilesQuery,
  ValueFilesQueryVariables
} from '~/types/graphql'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'
import FileField from '~/components/common/FileField.vue'

type ValueFile = {
  file: FileType
  deleted: boolean
}

export default defineComponent({
  components: { FileField },
  props: {
    valueType: { type: Object as PropType<ValueType>, default: null },
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
        valueId: props.valueType.id
      },
      options: {
        enabled: !!props.valueType
      }
    })

    const localValueFiles = ref<ValueFile[]>([])
    watch(valueFiles, (value) => {
      if (value) {
        localValueFiles.value = value.map((file: FileType) => ({ file, deleted: false }))
      }
    }, { immediate: true })

    const remainingExistFiles = computed<string[]>(
      () => localValueFiles.value.filter(valueFile => !valueFile.deleted).map(valueFile => valueFile.file.id)
    )

    const newValue = ref<string>(props.value)
    const newFiles = ref<File[]>([])

    const remainingFiles = computed<(string | File)[]>(() => [...remainingExistFiles.value, ...newFiles.value])
    watch(remainingFiles, (value) => {
      filesValidationProvider.value.validate(value)
    })

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    const clearValue = () => {
      active.value = false
      emit('set-value', '', {
        remainingFiles: [],
        newFiles: []
      })
    }

    const setValue = () => {
      active.value = false
      emit('set-value', newValue.value, {
        remainingFiles: remainingExistFiles.value,
        newFiles: newFiles.value
      })
    }

    return {
      t,
      active,
      filesValidationProvider,
      localValueFiles,
      newValue,
      newFiles,
      cancel,
      clearValue,
      setValue
    }
  }
})
</script>
