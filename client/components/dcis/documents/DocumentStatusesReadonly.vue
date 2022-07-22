<template lang="pug">
v-dialog(v-model="active" width="600" scrollable)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  v-card
    v-card-title {{ $t('dcis.documents.status.readonlyHeader') }}
      v-spacer
      v-btn(icon @click="active = false")
        v-icon mdi-close
    v-card-subtitle {{ String($t('dcis.documents.status.subheader', { version: document.version })) }}
    v-card-text
      v-list(two-line dense)
        v-list-item(v-for="item in documentStatuses" :key="item.id")
          v-list-item-content
            v-list-item-title {{ item.status.name }}
            v-list-item-subtitle {{ dateTimeHM(item.createdAt) }}
            v-list-item-subtitle {{ getUserName(item.user) }}
          v-list-item-content
            v-list-item-subtitle.font-italic {{ item.comment }}
</template>

<script lang="ts">
import { PropType } from '#app'
import { DocumentType, DocumentStatusesQuery, DocumentStatusesQueryVariables } from '~/types/graphql'
import { useCommonQuery, useFilters } from '~/composables'
import documentStatusesQuery from '~/gql/dcis/queries/document_statuses.graphql'

export default defineComponent({
  props: {
    document: { type: Object as PropType<DocumentType>, required: true }
  },
  setup (props) {
    const { dateTimeHM, getUserName } = useFilters()

    const active = ref<boolean>(false)

    const { data: documentStatuses } = useCommonQuery<
      DocumentStatusesQuery,
      DocumentStatusesQueryVariables
    >({
      document: documentStatusesQuery,
      variables: { documentId: props.document.id }
    })

    return { dateTimeHM, getUserName, active, documentStatuses }
  }
})
</script>
