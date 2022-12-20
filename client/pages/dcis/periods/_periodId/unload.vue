<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.unload.name') }}
  v-btn(:loading="unloadPeriodLoading" color="primary" @click="unloadPeriod") {{ $t('upload') }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, UnloadPeriodMutation, UnloadPeriodMutationVariables } from '~/types/graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import unloadPeriodMutation from '~/gql/dcis/mutations/period/unload_period.graphql'

type UnloadPeriodMutationResult = { data: UnloadPeriodMutation }

export default defineComponent({
  components: { LeftNavigatorContainer },
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.unload.name') as string,
        to: localePath({ name: 'dcis-periods-periodId-unload' }),
        exact: true
      }
    ]))

    const { mutate: unloadPeriodMutate, loading: unloadPeriodLoading, onDone: unloadPeriodOnDone } = useMutation<
      UnloadPeriodMutation,
      UnloadPeriodMutationVariables
    >(unloadPeriodMutation)
    unloadPeriodOnDone(({ data: { unloadPeriod: { success, src } } }: UnloadPeriodMutationResult) => {
      if (success) {
        window.open(src, '_blank')
      }
    })
    const unloadPeriod = () => {
      unloadPeriodMutate({ periodId: props.period.id })
    }

    return { bc, unloadPeriod, unloadPeriodLoading }
  }
})
</script>
