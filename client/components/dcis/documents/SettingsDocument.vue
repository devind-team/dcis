<template lang="pug">
v-menu(v-model="active" bottom left)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-list
    document-unload(:document="document" @close="close")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-download
          v-list-item-content {{ $t('dcis.documents.unloadDocument.name') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { DocumentType } from '~/types/graphql'
import DocumentUnload from '~/components/dcis/documents/DocumentUnload.vue'

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
