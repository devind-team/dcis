<template lang="pug">
  v-file-input(v-bind="$attrs" v-on="$listeners" v-model="computedValue")
    template(#selection v-if="existFileVisible")
      | {{ existingFile.name ? existingFile.name : $filters.basename(existingFile.src) }}
    template(#append-outer v-if="existFileVisible")
      v-tooltip(bottom)
        template(#activator="{ on }")
          v-btn(v-on="on" :href="`/${existingFile.src}`" target="_blank" icon small)
            v-icon mdi-download
        span {{ t('open') }}
    slot(v-for="slot in Object.keys($slots)" :name="slot" :slot="slot")
    template(v-for="slot in outerSlotNames" v-slot:[slot]="scope")
      slot(v-bind="scope" :name="slot")
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { PropType } from 'vue'

export type ExistingFile = {
  name?: string,
  src: string
}

@Component<FileField>({
  inheritAttrs: false,
  computed: {
    outerSlotNames (): string[] {
      return Object.keys(this.$scopedSlots).filter((key: string) => key !== 'selection')
    },
    existFileVisible (): boolean {
      return !(this.value || this.multiple || !this.existingFile)
    },
    computedValue: {
      get (): File | File[] | null | undefined {
        if (process.server || !this.existFileVisible) {
          return this.value
        }
        return new File([], '')
      },
      set (value: File | File[] | undefined): void {
        this.$emit('update:existingFile', null)
        this.$emit('input', value)
      }
    }
  }
})
export default class FileField extends Vue {
  @Prop({ type: [Object, Array] as PropType<File | File[]> }) value!: File | File[] | null | undefined
  @Prop({ type: Object as PropType<ExistingFile> }) existingFile!: ExistingFile | undefined
  @Prop({ type: Boolean, default: false }) multiple!: boolean

  readonly outerSlotNames!: string[]
  readonly existFileVisible!: boolean[]
  computedValue!: File | File[] | undefined

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`common.fileField.${path}`, values) as string
  }
}
</script>
