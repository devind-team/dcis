<template lang="pug">
  div(v-if="valueType === null") {{ value }}
  div(v-else)
    a(@click="openFile") {{ value }}
</template>

<script lang="ts">
import { useApolloClient } from '@vue/apollo-composable'
import { defineComponent } from '#app'
import type { PropType } from '#app'
import { ValueType, ValueFilesUrlQuery, ValueFilesUrlQueryVariables } from '~/types/graphql'
import valueFilesUrlQuery from '~/gql/dcis/queries/value_files_url.graphql'

export default defineComponent({
  props: {
    valueType: { type: Object as PropType<ValueType>, default: null },
    value: { type: String, default: null }
  },
  setup (props) {
    const apolloClient = useApolloClient()

    const openFile = async () => {
      const { data: { valueFilesUrl } } = await apolloClient.client.query<
        ValueFilesUrlQuery,
        ValueFilesUrlQueryVariables
      >({
        query: valueFilesUrlQuery,
        variables: {
          valueId: props.valueType.id
        }
      })
      window.open(valueFilesUrl, '_blank')
    }

    return { openFile }
  }
})
</script>
