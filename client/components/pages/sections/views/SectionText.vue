<template lang="pug">
  v-row(no-gutters style="position: relative")
    v-col
      editor-typography(:html="section.text")
      section-action(
        v-if="hasPerm(['pages.change_section', 'pages.delete_section'], true) || editSection"
        :section="section"
        :edit-section="editSection"
        :update-delete-section="updateDeleteSection"
      )
</template>

<script lang="ts">
import { defineComponent, PropType, toRefs } from '#app'
import { DataProxy } from 'apollo-cache'
import {
  DeleteSessionsMutationPayload,
  PageQuery,
  PageQueryVariables,
  PageType, SectionInterface,
  SectionTextType, UserType
} from '~/types/graphql'
import SectionAction from '~/components/pages/sections/actions/SectionAction.vue'
import EditorTypography from '~/components/common/editor/EditorTypography.vue'
import { HasPermissionFnType, useAuthStore } from '~/stores'

export default defineComponent({
  components: { EditorTypography, SectionAction },
  props: {
    page: { required: true, type: Object as PropType<PageType> },
    section: { required: true, type: Object as PropType<SectionTextType> }
  },
  setup (props) {
    const authStore = useAuthStore()
    const { user, loginIn, hasPerm } = toRefs<{ user: UserType, loginIn: boolean, hasPerm: HasPermissionFnType }>(authStore)

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
        data.page.sections = data.page.sections.filter((e: SectionInterface) => e.id !== this.section.id!)
        store.writeQuery({
          query: require('~/gql/pages/queries/page.graphql'),
          variables: { pageId: props.page.id },
          data
        })
      }
    }
    return { hasPerm, editSection, updateDeleteSection }
  }
})
</script>
