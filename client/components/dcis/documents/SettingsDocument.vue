<template lang="pug">
  v-menu(v-model="active" bottom left)
    template(#activator="{ on, attrs }")
      slot(name="activator" :on="on" :attrs="attrs")
    v-list
      document-unload(@close="close" :document-id="documentId")
        template(#activator="{ on, attrs }")
          v-list-item(v-on="on" v-bind="attrs")
            v-list-item-icon
              v-icon mdi-download
            v-list-item-content {{ $t('dcis.documents.unloading.name') }}
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import DocumentUnload from '~/components/dcis/documents/DocumentUnload.vue'

export default defineComponent({
  components: { DocumentUnload },
  props: {
    documentId: { type: String, required: true }
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
