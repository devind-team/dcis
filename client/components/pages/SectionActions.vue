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
import type { PropType, ComputedRef } from '#app'
import { computed, defineComponent, useNuxtApp } from '#app'
import { HasPermissionFnType } from '~/store/auth'
import { SectionInterface } from '~/types/graphql'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export default defineComponent({
  components: { DeleteMenu },
  props: {
    section: { type: Object as PropType<SectionInterface>, required: true }
  },
  setup () {
    const { $store } = useNuxtApp()
    const hasPerm: ComputedRef<HasPermissionFnType> = computed<HasPermissionFnType>(() => $store.getters['auth/hasPerm'])
    return { hasPerm }
  }
})
</script>
