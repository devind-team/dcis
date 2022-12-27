<template lang="pug">
left-navigator-container(:bread-crumbs="bc" fluid @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.unload.name') }}
  .d-flex.flex-column.align-start
    organization-filter(
      v-model="selectedOrganizations"
      :period="period"
      :title="String($t('dcis.periods.unload.organizationsFilterTitle'))"
      message-container-class="mb-2"
    )
    v-btn(:loading="unloadPeriodLoading" color="primary" @click="unloadPeriod") {{ $t('upload') }}
</template>

<script lang="ts">
import { ref, computed, defineComponent, PropType } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodType, OrganizationType, UnloadPeriodMutation, UnloadPeriodMutationVariables } from '~/types/graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import OrganizationFilter from '~/components/dcis/periods/OrganizationFilter.vue'
import unloadPeriodMutation from '~/gql/dcis/mutations/period/unload_period.graphql'

type UnloadPeriodMutationResult = { data: UnloadPeriodMutation }

export default defineComponent({
  components: { LeftNavigatorContainer, OrganizationFilter },
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

    const selectedOrganizations = ref<OrganizationType[]>([])

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

    return { bc, selectedOrganizations, unloadPeriod, unloadPeriodLoading }
  }
})
</script>
