<template lang="pug">
items-data-filter(
  ref="filter"
  v-model="selectedStatuses"
  :title="title || String($t('dcis.documents.statusFilter.title'))"
  :no-filtration-message="String($t('dcis.documents.statusFilter.noFiltrationMessage'))"
  :multiple-message-function="multipleMessageFunction"
  :items="statuses ? statuses : []"
  :get-name="status => status.name"
  :message-container-class="messageContainerClass"
  multiple
  has-select-all
)
</template>

<script lang="ts">
import { computed, defineComponent, nextTick, onMounted, PropType, ref, watch } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { Class } from '~/types/filters'
import { PeriodType, StatusesQuery, StatusesQueryVariables, StatusFieldsFragment, StatusType } from '~/types/graphql'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import statusesQuery from '~/gql/dcis/queries/statuses.graphql'

export default defineComponent({
  components: { ItemsDataFilter },
  props: {
    value: { type: Array as PropType<StatusType[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true },
    title: { type: String, default: null },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: null }
  },
  setup (props, { emit }) {
    const { tc } = useI18n()

    const filter = ref<InstanceType<typeof ItemsDataFilter> | null>(null)

    const selectedStatuses = computed<StatusType[]>({
      get () {
        return props.value
      },
      set (value: StatusType[]) {
        emit('input', value)
      }
    })

    const multipleMessageFunction = (name: string, restLength: number) =>
      tc('dcis.documents.statusFilter.multipleMessage', restLength, { name, restLength }) as string

    const { data: statuses } = useCommonQuery<
      StatusesQuery,
      StatusesQueryVariables
    >({
      document: statusesQuery
    })

    onMounted(() => {
      watch(() => statuses.value, (statuses: StatusFieldsFragment[]) => {
        if (props.period.isCurator && statuses) {
          const inputCompleted = statuses.find((status: StatusType) => status.name === 'Ввод завершен')
          if (inputCompleted) {
            nextTick(() => {
              filter.value.select([inputCompleted])
            })
          }
        }
        emit('statuses-loaded')
      }, { immediate: true })
    })

    return { filter, selectedStatuses, multipleMessageFunction, statuses }
  }
})
</script>
