<template lang="pug">
items-data-filter(
  v-model="selectedOrganizationKinds"
  :title="title || String($t('dcis.periods.organizationKindFilter.title'))"
  :no-filtration-message="String($t('dcis.periods.organizationKindFilter.noFiltrationMessage'))"
  :multiple-message-function="multipleMessageFunction"
  :items="items"
  :get-name="item => item.type"
  multiple
  has-select-all
)
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { Class } from '~/types/filters'
import {
  PeriodOrganizationKindsQuery,
  PeriodOrganizationKindsQueryVariables,
  PeriodType
} from '~/types/graphql'
import periodOrganizationKindsQuery from '~/gql/dcis/queries/period_organization_kinds.graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

export type OrganizationKindType = {
  id: string,
  type: string,
}

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<OrganizationKindType[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    title: { type: String, default: null },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null }
  },
  setup (props, { emit }) {
    const { tc } = useI18n()

    const selectedOrganizationKinds = computed<OrganizationKindType[]>({
      get () {
        return props.value
      },
      set (value: OrganizationKindType[]) {
        emit('input', value)
      }
    })

    const multipleMessageFunction = (name: string, restLength: number) =>
      tc('dcis.periods.organizationKindFilter.multipleMessage', restLength, { name, restLength }) as string

    const { data: periodOrganizationTypes } = useCommonQuery<
      PeriodOrganizationKindsQuery,
      PeriodOrganizationKindsQueryVariables
    >({
      document: periodOrganizationKindsQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    const items = computed<OrganizationKindType[]>(() => periodOrganizationTypes.value
      ? periodOrganizationTypes.value.map((type: string, index: number) => ({
        id: String(index),
        type
      }))
      : []
    )

    return { selectedOrganizationKinds, multipleMessageFunction, items }
  }
})
</script>
