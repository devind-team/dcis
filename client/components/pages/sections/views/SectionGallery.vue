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
import { Vue, Component, Prop } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { DataProxy } from 'apollo-cache'
import {
  DeleteSessionsMutationPayload,
  PageQuery,
  PageQueryVariables,
  PageType, SectionGalleryType, SectionInterface,
  UserType
} from '~/types/graphql'
import ImageGallery from '~/components/common/ImageGallery.vue'
import SectionAction from '~/components/pages/sections/actions/SectionAction.vue'

@Component<SectionGallery>({
  components: { SectionAction, ImageGallery },
  computed: {
    ...mapGetters({ user: 'auth/user', loginIn: 'auth/loginIn', hasPerm: 'auth/hasPerm' }),
    editSection (): boolean {
      return this.loginIn && [this.page.user?.id, this.section.user.id].includes(this.user.id)
    }
  }
})
export default class SectionGallery extends Vue {
  @Prop({ required: true }) page!: PageType
  @Prop({ required: true }) section!: SectionGalleryType

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
