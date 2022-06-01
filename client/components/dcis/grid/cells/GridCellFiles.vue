<template lang="pug">
  v-dialog(v-model="active" width="600px" persistent)
    template(#activator="{ on }")
      div(v-on="on") {{ value }}
    v-card
      v-card-title {{ t('dcis.grid.changeValue') }}
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
              span {{ t(localFile.deleted ? 'cancelDeletion' : 'delete') }}
          v-list-item-content
            v-list-item-title
              nuxt-link(
                :to="`/${localFile.file.src}`"
                :class="{ 'text-decoration-line-through': localFile.deleted }"
                target="_blank"
              ) {{ localFile.file.name }}
        v-file-input(
          v-model="newFiles"
          :label="t('dcis.grid.cellFiles.newFiles')"
          chips
          clearable
          multiple
        )
      v-card-actions
        v-btn(
          v-if="existingFiles.length"
          color="success"
          @click="$emit('unload-archive')"
        ) {{ t('dcis.grid.cellFiles.uploadArchive') }}
        v-spacer
        v-btn(color="primary" @click="setValue") {{ t('save') }}
</template>

<script lang="ts">
import { PropType } from '#app'
import type { FileType } from '~/types/graphql'
import FileField from '~/components/common/FileField.vue'

type ValueFile = {
  file: FileType
  deleted: boolean
}

export default defineComponent({
  components: { FileField },
  props: {
    files: { type: Array as PropType<FileType[]>, required: true },
    value: { type: String, default: null }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const active = ref<boolean>(true)

    const existingFiles = ref<ValueFile[]>([])
    watch(() => props.files, (value) => {
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
      emit(
        'set-value',
        remainingFiles.value.length + newFiles.value.length ? t('yes') : t('no'),
        remainingFiles.value,
        newFiles.value
      )
    }

    return {
      t,
      active,
      existingFiles,
      newFiles,
      cancel,
      setValue
    }
  }
})
</script>
