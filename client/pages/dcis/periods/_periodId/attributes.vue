<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.links.attributes') }}
  v-row(v-if="!loading")
    v-col
      pre {{ attributes }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { AttributesQuery, AttributesQueryVariables, PeriodType } from '~/types/graphql'
import attributesQuery from '~/gql/dcis/queries/attributes.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'

export default defineComponent({
  components: { LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.links.attributes') as string,
        to: localePath({ name: 'dcis-periods-periodId-attributes' }),
        exact: true
      }
    ]))

    const { data: attributes, loading } = useCommonQuery<AttributesQuery, AttributesQueryVariables, 'attributes'>({
      document: attributesQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    return { bc, attributes, loading }
  }
})
</script>
