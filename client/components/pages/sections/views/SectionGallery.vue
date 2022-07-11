<template lang="pug">
v-row(style="position:relative")
  v-col
    p.text-h5.text-center {{section.text}}
    image-gallery(:images="section.images.map(e => `/${e.src}`)")
    section-action(
      v-if="hasPerm(['pages.change_section', 'pages.delete_section'], true) || editSection"
      :section="section"
      :edit-section="editSection"
      :update-delete-section="updateDeleteSection"
    )
</template>

<script lang="ts">
import { defineComponent, PropType, toRefs, computed } from '#app'

import { DataProxy } from 'apollo-cache'
import {
  DeleteSessionsMutationPayload,
  PageQuery,
  PageQueryVariables,
  PageType, SectionGalleryType, SectionInterface,
  UserType
} from '~/types/graphql'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import ImageGallery from '~/components/common/ImageGallery.vue'
import SectionAction from '~/components/pages/sections/actions/SectionAction.vue'

export default defineComponent({
  components: { SectionAction, ImageGallery },
  props: {
    page: { required: true, type: Object as PropType<PageType> },
    section: { required: true, type: Object as PropType<SectionGalleryType> }
  },
  setup (props) {
    const authStore = useAuthStore()
    const { user, hasPerm, loginIn } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType, loginIn: boolean }>(authStore)

    const editSection = computed(() => {
      return loginIn.value && [props.page.user?.id, props.section.user.id].includes(user.value.id)
    })
    const updateDeleteSection = (store: DataProxy, { data: { deleteSection: { success } } }: { data: { deleteSection: DeleteSessionsMutationPayload } }) => {
      if (success) {
        const data: PageQuery = store.readQuery<PageQuery, PageQueryVariables>({
          query: require('~/gql/pages/queries/page.graphql'),
          variables: { pageId: props.page.id }
        })!
        // @ts-ignore
        data.page.sections = data.page.sections.filter((e: SectionInterface) => e.id !== props.section.id!)
        store.writeQuery({
          query: require('~/gql/pages/queries/page.graphql'),
          variables: { pageId: props.page.id },
          data
        })
      }
    }
    return { hasPerm, updateDeleteSection, editSection }
  }
})
</script>
