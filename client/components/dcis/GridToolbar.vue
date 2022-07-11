<template lang="pug">
v-toolbar(height="100" elevation="2")
  .d-flex.flex-column(style="width: 100%")
    .d-flex.align-center
      v-toolbar-title.mr-1 {{ document.comment }}
      v-tooltip(bottom)
        template(#activator="{ on }")
          v-btn(v-on="on" color="success" fab small icon)
            v-icon mdi-download
        span {{ t('download') }}
    .d-flex.align-center
      v-btn-toggle.mt-2(v-model="activeSheetIndex" dense)
        v-btn(v-for="sheet in document.sheets" :key="sheet.id") {{ sheet.name }}
      v-spacer
      v-btn(color="primary") {{ t('dcis.grid.toolbar.addRow') }}
</template>

<script lang="ts">
import { defineComponent, computed } from '#app'
import type { PropType } from '#app'
import type { DocumentType, SheetType } from '~/types/graphql'
import { useI18n } from '~/composables'

export default defineComponent({
  props: {
    document: {
      type: Object as PropType<DocumentType>,
      required: true
    },
    value: {
      type: Object as PropType<SheetType>,
      default: null
    }
  },
  setup (props, { emit }) {
    const { t } = useI18n()

    const activeSheetIndex = computed({
      get: () => props.document.sheets.findIndex(sheet => sheet.id === props.value?.id),
      set: value => emit('input', props.document.sheets[value])
    })

    return {
      t,
      activeSheetIndex
    }
  }
})
</script>
