<template lang="pug">
  v-row
    v-col
      v-btn-toggle(dense)
        v-btn #[v-icon mdi-format-align-left]
        v-btn #[v-icon mdi-format-align-center]
        v-btn #[v-icon mdi-format-align-right]
      v-btn-toggle.ml-1(multiple dense)
        v-btn #[v-icon mdi-format-bold]
        v-btn #[v-icon mdi-format-italic]
        v-btn #[v-icon mdi-format-underline]
    v-col
      v-combobox.flex(:items="kinds" dense style="width: 150px")
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent } from '#app'
import { useI18n } from '~/composables'
import { cellKinds } from '~/composables/grid'

type DocumentUpdateType = (cache: any, result: any, transform: (dc: any, result: any) => any) => any

export default defineComponent({
  props: {
    update: { type: Function as PropType<DocumentUpdateType>, required: true }
  },
  setup () {
    const { t } = useI18n()
    const kinds: ComputedRef = computed(() => (Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.cellKinds.${k}`), value: k }))))
    return { kinds }
  }
})
</script>
