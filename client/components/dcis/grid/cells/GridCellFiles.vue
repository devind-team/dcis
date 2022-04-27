<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    v-card
      v-card-title {{ $t('dcis.cells.gridCellFiles.title') }}
        v-spacer
        v-btn(@click="cancel" icon)
          v-icon mdi-close
      v-card-text
        v-list-item.px-0(
          v-for="localFile in existingFiles"
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
              span {{ $t(localFile.deleted ? 'cancelDeletion' : 'delete') }}
          v-list-item-content
            v-list-item-title
              nuxt-link(
                :to="`/${localFile.file.src}`"
                :class="{ 'text-decoration-line-through': localFile.deleted }"
                target="_blank"
              ) {{ localFile.file.name }}
        v-file-input(
          v-model="newFiles"
          :label="$t('dcis.cells.gridCellFiles.newFiles')"
          chips
          clearable
          multiple
        )
      v-card-actions
        v-btn(
          v-if="existingFiles.length"
          color="success"
          @click="uploadArchive"
        ) {{ $t('dcis.cells.gridCellFiles.uploadArchive') }}
        v-spacer
        v-btn(color="primary" @click="setValue") {{ $t('save') }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from '@apollo/client'
import type { PropType } from '#app'
import {
  FileType,
  ValueType,
  UnloadFileValueArchiveMutation,
  UnloadFileValueArchiveMutationVariables,
  ValueFilesQuery,
  ValueFilesQueryVariables
} from '~/types/graphql'
import valueFilesQuery from '~/gql/dcis/queries/value_files.graphql'
import unloadFileValueArchiveMutation from '~/gql/dcis/mutations/sheet/unload_file_value_archive.graphql'
import FileField from '~/components/common/FileField.vue'
import type { ChangeFileValueMutationResult } from '~/components/dcis/grid/GridCell.vue'

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

    const variables = ref<
      UnloadFileValueArchiveMutationVariables |
      ValueFilesQueryVariables
    >(props.valueType ? { valueId: props.valueType.id } : { valueId: '' })

    const { mutate: unloadFileValueArchiveMutate } = useMutation<
      UnloadFileValueArchiveMutation,
      UnloadFileValueArchiveMutationVariables
    >(unloadFileValueArchiveMutation, {
      variables: variables.value
    })

    const uploadArchive = async () => {
      const { data: { unloadFileValueArchive: { src } } } = await unloadFileValueArchiveMutate()
      window.open(src, '_blank')
    }

    const {
      data: valueFiles,
      update: valueFilesUpdate
    } = useCommonQuery<ValueFilesQuery, ValueFilesQueryVariables, 'valueFiles'>({
      document: valueFilesQuery,
      variables: variables.value,
      options: {
        enabled: !!props.valueType
      }
    })

    const updateValueFiles = (
      cache: DataProxy,
      result: ChangeFileValueMutationResult
    ) => {
      if (props.valueType) {
        valueFilesUpdate(cache, result, (dataCache) => {
          const mutationResult = result.data.changeFileValue
          const dataKey = Object.keys(dataCache)[0]
          dataCache[dataKey] = mutationResult[dataKey]
          return dataCache
        })
      }
    }

    const existingFiles = ref<ValueFile[]>([])
    watch(valueFiles, (value) => {
      if (value) {
        existingFiles.value = value.map((file: FileType) => ({ file, deleted: false }))
      }
    }, { immediate: true })

    const remainingFiles = computed<string[]>(
      () => existingFiles.value.filter(valueFile => !valueFile.deleted).map(valueFile => valueFile.file.id)
    )

    const newFiles = ref<File[]>([])

    const cancel = () => {
      active.value = false
      emit('cancel')
    }

    const setValue = () => {
      active.value = false
      emit('set-value', remainingFiles.value.length + newFiles.value.length ? t('yes') : t('no'), {
        remainingFiles: remainingFiles.value,
        newFiles: newFiles.value
      }, updateValueFiles)
    }

    return {
      active,
      uploadArchive,
      existingFiles,
      newFiles,
      cancel,
      setValue
    }
  }
})
</script>
