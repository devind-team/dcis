<template lang="pug">
v-menu(v-model="active" offset-y)
  template(#activator="{ on, attrs }")
    v-btn.grid-sheet-menu__button(
      v-on="on"
      v-bind="attrs"
      elevation="0"
      tile
    ) {{ $t('dcis.grid.sheetMenu.documentUnloadMenu.buttonText') }}
  v-list(dense)
    document-unload(:document="document" @close="close")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-title {{ $t('dcis.grid.sheetMenu.documentUnloadMenu.unload') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import DocumentUnload from '~/components/dcis/documents/DocumentUnload.vue'
import { DocumentType } from '~/types/graphql'

export default defineComponent({
  components: { DocumentUnload },
  props: {
    document: { type: Object as PropType<DocumentType>, required: true }
  },
  setup (_, { emit }) {
    const active = ref<boolean>(false)

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, close }
  }
})
</script>
