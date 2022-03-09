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
import { Vue, Component, Prop } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { DataProxy } from 'apollo-cache'
import {
  DeleteSessionsMutationPayload,
  PageQuery,
  PageQueryVariables,
  PageType, SectionInterface,
  SectionTextType,
  UserType
} from '~/types/graphql'
import SectionAction from '~/components/pages/sections/actions/SectionAction.vue'
import EditorTypography from '~/components/common/editor/EditorTypography.vue'

@Component<SectionText>({
  components: { EditorTypography, SectionAction },
  computed: {
    ...mapGetters({ user: 'auth/user', loginIn: 'auth/loginIn', hasPerm: 'auth/hasPerm' }),
    editSection (): boolean {
      return this.loginIn && [this.page.user?.id, this.section.user.id].includes(this.user.id)
    }
  }
})
export default class SectionText extends Vue {
  @Prop({ required: true }) page!: PageType
  @Prop({ required: true }) section!: SectionTextType

  user!: UserType
  loginIn!: boolean

  updateDeleteSection (store: DataProxy, { data: { deleteSection: { success } } }: { data: { deleteSection: DeleteSessionsMutationPayload } }) {
    if (success) {
      const data: PageQuery = store.readQuery<PageQuery, PageQueryVariables>({
        query: require('~/gql/pages/queries/page.graphql'),
        variables: { pageId: this.page.id }
      })!
      // @ts-ignore
      data.page.sections = data.page.sections.filter((e: SectionInterface) => e.id !== this.section.id!)
      store.writeQuery({
        query: require('~/gql/pages/queries/page.graphql'),
        variables: { pageId: this.page.id },
        data
      })
    }
  }
}
</script>
