<template lang="pug">
bread-crumbs(:items="bc")
  apollo-mutation(
    v-slot="{ mutate, loading, error }"
    :mutation="require('~/gql/dcis/mutations/period/unload_period.graphql')"
    :variables="variables"
    @done="unloadPeriodOnDone"
    tag
  )
    v-card
      v-card-title.pb-0
        v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
        | {{ $t('dcis.periods.unload.name') }}
      form(@submit.prevent="mutate")
        v-card-text
          organization-filter(
            v-model="selectedOrganizations"
            :period="period"
            :title="String($t('dcis.periods.unload.organizationsFilterTitle'))"
            message-container-class="mr-1"
          )
          status-filter(
            v-model="selectedStatuses"
            :period="period"
            :title="String($t('dcis.periods.unload.statusFilterTitle'))"
            message-container-class="mr-1"
          )
          v-checkbox(v-model="unloadWithoutDocument" :label="$t('dcis.periods.unload.unloadWithoutDocument')")
          v-checkbox(v-model="applyNumberFormat" :label="$t('dcis.periods.unload.applyNumberFormat')")
          v-text-field(v-model="emptyCell" :label="$t('dcis.periods.unload.emptyCell')")
        v-card-actions
          v-btn(:loading="loading" type="submit" color="primary") {{ $t('upload') }}
</template>

<script lang="ts">
import { ref, computed, defineComponent, PropType } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  PeriodType,
  OrganizationType,
  StatusType,
  UnloadPeriodMutation,
  UnloadPeriodMutationVariables
} from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import OrganizationFilter from '~/components/dcis/periods/OrganizationFilter.vue'
import StatusFilter from '~/components/dcis/periods/StatusFilter.vue'

type UnloadPeriodMutationResult = { data: UnloadPeriodMutation }

export default defineComponent({
  components: { BreadCrumbs, OrganizationFilter, StatusFilter },
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
    const selectedStatuses = ref<StatusType[]>([])
    const unloadWithoutDocument = ref<boolean>(true)
    const applyNumberFormat = ref<boolean>(true)
    const emptyCell = ref<string>('')

    const variables = computed<UnloadPeriodMutationVariables>(() => ({
      periodId: props.period.id,
      organizationIds: selectedOrganizations.value.map((organization: OrganizationType) => organization.id),
      statusIds: selectedStatuses.value.map((status: StatusType) => status.id),
      unloadWithoutDocument: unloadWithoutDocument.value,
      applyNumberFormat: applyNumberFormat.value,
      emptyCell: emptyCell.value
    }))

    const unloadPeriodOnDone = ({ data: { unloadPeriod: { success, src } } }: UnloadPeriodMutationResult) => {
      if (success) {
        window.open(src, '_blank')
      }
    }

    return {
      bc,
      selectedOrganizations,
      selectedStatuses,
      unloadPeriodOnDone,
      unloadWithoutDocument,
      applyNumberFormat,
      emptyCell,
      variables
    }
  }
})
</script>
