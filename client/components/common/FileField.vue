<template lang="pug">
  v-file-input(v-bind="$attrs" v-on="$listeners" v-model="computedValue")
    template(#selection v-if="existFileVisible")
      | {{ existingFile.name ? existingFile.name : basename(existingFile.src) }}
    template(#append-outer v-if="existFileVisible")
      v-tooltip(bottom)
        template(#activator="{ on }")
          v-btn(v-on="on" :href="`/${existingFile.src}`" target="_blank" icon small)
            v-icon mdi-download
        span {{ $t('common.fileField.open') }}
    slot(v-for="slot in Object.keys($slots)" :name="slot" :slot="slot")
    template(v-for="slot in outerSlotNames" v-slot:[slot]="scope")
      slot(v-bind="scope" :name="slot")
</template>

<script lang="ts">
import { VueConstructor } from 'vue'
import type { PropType } from '#app'
import { computed, defineComponent, getCurrentInstance } from '#app'
import { useFilters } from '~/composables'

export type ExistingFile = {
  name?: string,
  src: string
}
type FileTypeInput = File | File[] | null

export default defineComponent({
  inheritAttrs: false,
  props: {
    value: { type: [Object, Array] as PropType<FileTypeInput>, default: null },
    existingFile: { type: Object as PropType<ExistingFile | null>, default: null },
    multiple: { type: Boolean, default: false }
  },
  setup (props, { emit }) {
    const { basename } = useFilters()
    const instance = getCurrentInstance()
    const vm = instance?.proxy || instance as unknown as InstanceType<VueConstructor>

    const outerSlotNames = computed<string[]>(() => (
      Object.keys(vm.$scopedSlots).filter((key: string) => key !== 'selection')
    ))

    const existFileVisible = computed<boolean>(() => (!(props.value || props.multiple || !props.existingFile)))

    const computedValue = computed<FileTypeInput>({
      get: (): File | File[] | null => {
        if (process.server || !existFileVisible.value) {
          return props.value
        }
        return new File([], '')
      },
      set: (value: FileTypeInput) => {
        emit('update:existingFile', null)
        emit('input', value)
      }
    })

    return { basename, outerSlotNames, existFileVisible, computedValue }
  }
})
</script>
