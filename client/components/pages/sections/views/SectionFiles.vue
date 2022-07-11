<template lang="pug">
v-row(style="position:relative")
  v-col
    p.text-h5.text-center {{section.text}}
    v-data-iterator(:items="section.files" disable-pagination hide-default-footer)
      template(#header)
        v-sheet(v-html="section.text")
      template(#default="{ items }")
        v-list
          v-list-item(v-for="file in items" :key="file.id" :href="`/${file.src}`" target="_blank")
            v-list-item-content
              v-list-item-title {{ file.name }}
              v-list-item-subtitle {{ (file.size / 1024).toFixed(2) }} {{ $t('pages.components.sectionFiles.mb') }}
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
  PageQueryVariables, PageType,
  SectionFilesType,
  SectionInterface,
  UserType
} from '~/types/graphql'
import EditorTypography from '~/components/common/editor/EditorTypography.vue'
import SectionAction from '~/components/pages/sections/actions/SectionAction.vue'
import { HasPermissionFnType, useAuthStore } from '~/stores'

export default defineComponent({
  components: { EditorTypography, SectionAction },
  props: {
    page: { required: true, type: Object as PropType<PageType> },
    section: { required: true, type: Object as PropType<SectionFilesType> }
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
    return { hasPerm, editSection, updateDeleteSection }
  }
})
</script>
