<template lang="pug">
  v-dialog(v-model="drawer" width="600")
    template(#activator="{ on }")
      slot(:on="on")
    apollo-mutation(
      :mutation="require('~/gql/pages/mutations/page/change_page_kind.graphql')"
      :variables="{ pageId: page.id, pageKindId }"
      @done="changePageKindDone"
      v-slot="{ mutate, loading, error }"
    )
      form(@submit.prevent="mutate()")
        v-card
          v-card-title {{ $t('pages.page.changeKind.header') }}
            v-spacer
            v-btn(@click="close" icon)
              v-icon mdi-close
          v-card-text
            v-alert(type="error" :value="!!error" dismissible) {{ error }}
            v-select(
              v-model="pageKindId"
              :items="pageKindList"
              :label="$t('pages.page.changeKind.kind')"
              :loading="$apollo.queries.pageKinds.loading"
              item-text="name"
              item-value="id"
            )
          v-card-actions
            v-spacer
            v-btn(
              :loading="loading"
              type="submit"
              color="primary"
            ) {{ $t('pages.page.changeKind.change') }}
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { PageType, PageKindType, ChangePageKindMutation } from '~/types/graphql'

@Component<ChangePageKind>({
  computed: {
    pageKindList () {
      return [
        { id: null, name: this.$t('pages.components.addPage.common') },
        ...this.pageKinds
      ]
    }
  },
  apollo: {
    pageKinds: require('~/gql/pages/queries/page_kinds.graphql')
  }
})
export default class ChangePageKind extends Vue {
  @Prop({ required: true, type: Object }) readonly page!: PageType

  drawer: boolean = false

  pageKindId!: string | null
  pageKinds!: PageKindType[]
  pageKindList!: PageKindType[]

  changePageKindDone ({ data: { changePageKind: { success } } }: { data: ChangePageKindMutation }) {
    if (success) {
      this.close()
    }
  }

  data () {
    return {
      pageKindId: this.page.kind != null ? this.page.kind.id : null
    }
  }

  close () {
    this.drawer = false
    this.pageKindId = this.page.kind != null ? this.page.kind.id : null
    this.$emit('close')
  }
}
</script>
