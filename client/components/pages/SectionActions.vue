<template lang="pug">
  v-menu(transition="scale-transition" origin="top left")
    template(v-slot:activator="{ on }")
      v-btn(v-on="on" icon absolute top right)
        v-icon mdi-dots-horizontal
    v-list
      v-list-item(@click="")
        v-list-item-icon #[v-icon mdi-file-document-edit-outline]
        v-list-item-content
          v-list-item-title {{ $t('pages.components.sectionActions.change') }}
      v-list-item(@click="")
        v-list-item-icon #[v-icon mdi-delete]
        v-list-item-content
          v-list-item-title {{ $t('pages.components.sectionActions.delete') }}
</template>
<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { useAuthStore } from '~/store'
import { SectionInterface } from '~/types/graphql'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export default defineComponent({
  components: { DeleteMenu },
  props: {
    section: { type: Object as PropType<SectionInterface>, required: true }
  },
  setup () {
    const authStore = useAuthStore()
    const hasPerm = toRef(authStore, 'hasPerm')
    return { hasPerm }
  }
})
</script>
