<template lang="pug">
  v-toolbar(height="100")
    .d-flex.flex-column
      .d-flex.align-center
        v-toolbar-title.mr-1 {{ document.name }}
        v-btn(color="success" fab small icon)
          v-icon mdi-download
      v-btn-toggle.mt-2(v-model="activeSheetIndex" dense)
        v-btn(v-for="sheet in document.sheets" :key="sheet.id") {{ sheet.name }}
    v-spacer
    grid-toolbar-avatar(
      v-for="documentUser in document.users"
      :key="documentUser.id"
      :document-user="documentUser"
    ).mr-2
</template>

<script lang="ts">
import { defineComponent, computed } from '#app'
import type { PropType } from '#app'
import type { DocumentType, SheetType } from '~/types/dcis'
import GridToolbarAvatar from '~/components/dcis/GridToolbarAvatar.vue'

export default defineComponent({
  components: {
    GridToolbarAvatar
  },
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
    const activeSheetIndex = computed({
      get: () => props.document.sheets.findIndex(sheet => sheet.id === props.value?.id),
      set: value => emit('input', props.document.sheets[value])
    })

    return {
      activeSheetIndex
    }
  }
})
</script>
