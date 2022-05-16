<template lang="pug">
  v-menu(v-model="active" transition="scale-transition" origin="top left")
    template(v-slot:activator="{ on }")
      v-btn(v-on="on" icon absolute top right)
        v-icon mdi-dots-horizontal
    v-list
      v-list-item(
        v-if="hasPerm('pages.change_section') || editSection"
        :to="localePath({ name: 'pages-pageId-section-sectionId', params: { sectionId: String(section.id) } })"
      )
        v-list-item-icon #[v-icon mdi-file-document-edit-outline]
        v-list-item-content
          v-list-item-title {{ $t('pages.components.sectionTextAction.changeText') }}
      apollo-mutation(
        :mutation="require('~/gql/pages/mutations/section/delete_section.graphql')"
        :variables="{ sectionId: section.id }"
        :update="updateDeleteSection"
      )
        template(v-slot="{ mutate }")
          delete-menu(v-slot="{ on }" @confirm="mutate" @cancel="active = false" item-name="секцию")
            v-list-item(v-on="on")
              v-list-item-icon #[v-icon mdi-delete]
              v-list-item-content
                v-list-item-title {{ $t('pages.components.sectionTextAction.delete') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { Ref, PropType } from '#app'
import { defineComponent, ref, toRefs } from '#app'
import type { HasPermissionFnType } from '~/stores'
import { useAuthStore } from '~/stores'
import { SectionInterface, UserType } from '~/types/graphql'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export default defineComponent({
  components: { DeleteMenu },
  props: {
    section: { type: Object as PropType<SectionInterface>, required: true },
    editSection: { type: Boolean, default: false },
    updateDeleteSection: { type: Function as PropType<(store: DataProxy, result: any) => void>, required: true }
  },
  setup () {
    const autStore = useAuthStore()

    const active: Ref<boolean> = ref<boolean>(false)
    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(autStore)

    return { active, user, hasPerm }
  }
})
</script>
