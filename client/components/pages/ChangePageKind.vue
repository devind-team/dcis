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
import type { PropType } from '#app'
import { computed, defineComponent, ref } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { PageType, ChangePageKindMutation, PageKindsQueryVariables, PageKindsQuery } from '~/types/graphql'
import pageKindsQuery from '~/gql/pages/queries/page_kinds.graphql'

export default defineComponent({
  props: {
    page: { type: Object as PropType<PageType>, required: true }
  },
  setup (props, { emit }) {
    const { t } = useI18n()
    const drawer = ref<boolean>(false)
    const pageKindId = ref<string | null>(props.page.kind?.id)

    const { data: pageKinds } = useCommonQuery<PageKindsQuery, PageKindsQueryVariables>({
      document: pageKindsQuery
    })

    const pageKindList = computed(() => ([
      { id: null, name: t('pages.components.addPage.common') },
      ...pageKinds.value
    ]))

    const changePageKindDone = ({ data: { changePageKind: { success } } }: { data: ChangePageKindMutation }) => {
      if (success) {
        close()
      }
    }

    const close = () => {
      drawer.value = false
      pageKindId.value = props.page.kind?.id
      emit('close')
    }

    return { drawer, pageKindId, pageKinds, pageKindList, close, changePageKindDone }
  }
})
</script>
